"""Includes StopWatch class."""
import time

from organon.fl.core.helpers import process_info_helper


class StopWatch:
    """Class for tracking execution time between lines."""

    def __init__(self, start: bool = False, with_cpu_times=False):
        self.initial_time = None
        self.with_cpu_times = with_cpu_times
        self.initial_cpu_times = None
        if start:
            self.start()

    def start(self):
        """Starts the timer."""
        self.initial_time = time.time()
        if self.with_cpu_times:
            self.initial_cpu_times = process_info_helper.get_cpu_times()

    def get_elapsed_seconds(self, restart: bool = False):
        """Returns the time(in seconds) passed since last re/start."""
        retval = time.time() - self.initial_time
        if restart:
            self.restart()
        return retval

    def get_cpu_times(self, restart: bool = False):
        """Gets cpu times used since start."""
        if not self.with_cpu_times:
            return None
        curr_cpu_times = process_info_helper.get_cpu_times()
        if restart:
            self.restart()
        return curr_cpu_times[0] - self.initial_cpu_times[0], curr_cpu_times[1] - self.initial_cpu_times[1]

    def restart(self):
        """Restarts timer."""
        self.initial_time = time.time()
        if self.with_cpu_times:
            self.initial_cpu_times = process_info_helper.get_cpu_times()
