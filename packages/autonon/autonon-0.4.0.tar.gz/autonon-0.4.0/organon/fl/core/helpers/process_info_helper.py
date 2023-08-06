"""Includes helper functions about operating system utilities."""
import os
from typing import Tuple

import psutil

from organon.fl.core.helpers import environment_info_helper
from organon.fl.generic.enums.os_type_id import OsType

OS_TYPE = environment_info_helper.get_os_type()

if OS_TYPE == OsType.LINUX:
    import resource  # pylint: disable=import-error


def get_memory_usage(process: psutil.Process = None) -> int:
    """Returns memory used by given process(current process if argument is None) in bytes"""
    if process is None:
        process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_peak_memory_usage(process: psutil.Process = None) -> int:
    """Returns peak memory usage of process in bytes"""

    if process is None:
        process = psutil.Process(os.getpid())

    if OS_TYPE == OsType.WINDOWS:
        return process.memory_info().peak_wset
    if OS_TYPE == OsType.LINUX:
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    raise NotImplementedError


def get_cpu_times(process: psutil.Process = None) -> Tuple[float, float]:
    """Returns user/system cpu times utilized by current process"""
    if process is None:
        process = psutil.Process(os.getpid())
    cpu_times = process.cpu_times()
    return cpu_times.user, cpu_times.system


def get_cpu_percentage_since_last_call(process: psutil.Process):
    """Returns cpu utilization percentage of process since last call of this method"""
    return process.cpu_percent() / psutil.cpu_count()
