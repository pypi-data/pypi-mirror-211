"""This module includes RuntimeStatsService class."""
import os
import time
from datetime import datetime
from threading import Thread

import psutil

from organon.afe.domain.reporting.runtime_statistics import RuntimeStatistics
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.executionutil.objects.stopwatch import StopWatch
from organon.fl.core.helpers import process_info_helper


class RuntimeStatsService:
    """Class for generating runtime statistics."""

    def __init__(self):
        self.__runtime_stats_thread: Thread = None
        self.__runtime_stats_thread_running = False
        self.__runtime_statistics: RuntimeStatistics = RuntimeStatistics()
        self.__watch: StopWatch = StopWatch(with_cpu_times=True)

    @property
    def runtime_statistics(self):
        """returns recorded runtime statistics"""
        return self.__runtime_statistics

    @property
    def is_running(self):
        """Returns if service is started or not"""
        return self.__runtime_stats_thread_running

    @property
    def is_thread_alive(self):
        """Returns if runtime stats thread is alive"""
        return self.__runtime_stats_thread.is_alive() if self.__runtime_stats_thread is not None else False

    def __record_runtime_stats(self, interval_in_seconds: int):
        process = psutil.Process(os.getpid())
        while self.__runtime_stats_thread_running:
            cpu_perc = process_info_helper.get_cpu_percentage_since_last_call(process)
            mem_usage = process_info_helper.get_memory_usage()
            stat_time = datetime.now()
            self.__runtime_statistics.cpu_usage[stat_time] = cpu_perc
            self.__runtime_statistics.memory_usage[stat_time] = mem_usage / (1024 * 1024)
            time.sleep(interval_in_seconds)

    def start_recording_runtime_stats(self, interval_in_seconds: float = 1):
        """Starts recording runtime statistics"""
        if self.__runtime_stats_thread_running:
            raise KnownException("Runtime stats service is already running")
        self.__runtime_stats_thread = Thread(target=self.__record_runtime_stats, args=(interval_in_seconds,))
        self.__runtime_stats_thread_running = True
        self.__runtime_stats_thread.start()
        self.__watch.start()

    def stop_recording_runtime_stats(self):
        """Stops recording runtime statistics"""
        if self.__runtime_stats_thread_running:
            self.__runtime_stats_thread_running = False
            self.__runtime_stats_thread.join()
            self.__runtime_statistics.execution_time = self.__watch.get_elapsed_seconds()
            cpu_times = self.__watch.get_cpu_times()
            self.__runtime_statistics.user_cpu_time = cpu_times[0]
            self.__runtime_statistics.system_cpu_time = cpu_times[1]

    def add_event(self, key, event_time=None):
        """Adds event to runtime stats"""
        if event_time is None:
            event_time = datetime.now()
        self.__runtime_statistics.event_times[key] = event_time
