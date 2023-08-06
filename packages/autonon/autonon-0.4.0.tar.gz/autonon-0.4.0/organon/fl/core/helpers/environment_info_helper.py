"""
This class keeps the helper functions that are used in gaining information about the environment.
"""
import getpass
import logging
import os
import platform
import signal
import socket
from typing import List

import psutil

from organon.fl.core.helpers import string_helper
from organon.fl.generic.datadtos.environment_info_dto import EnvironmentInfoDto
from organon.fl.generic.datadtos.process_info_dto import ProcessInfoDto
from organon.fl.generic.enums.os_type_id import OsType


def get_environment_info_dto() -> EnvironmentInfoDto:
    """
    Returns the information about environment.
    :return: Information about environment
    """
    dto: EnvironmentInfoDto = EnvironmentInfoDto(get_machine_name(), get_user_name())
    return dto


def get_machine_name() -> str:
    """
    Returns the machine name.
    :return: machine name
    """
    host_name: str = ""
    try:
        host_name = socket.gethostname()
    except (ValueError, TypeError) as ex:
        logging.error("Hostname can not be resolved")
        logging.error(ex)
    return host_name


def get_ipv4_address() -> str:
    """
    Returns the ipv4 address.
    :return: ipv4 address
    """
    ip_address: str = ""
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
    except (ValueError, TypeError, socket.gaierror) as ex:
        logging.error("IpAddress can not be resolved")
        logging.error(ex)
    return ip_address


def get_user_name() -> str:
    """
    Returns user name.
    :return: user name
    """
    user_name: str = getpass.getuser()
    return user_name


def get_process_by_process_id(process_id: int) -> ProcessInfoDto:
    """
    Returns process according to the process id.
    :param process_id: id of the process
    :return: information about Process
    """
    current_process_list: list = get_process_list("")
    for dto in current_process_list:
        if dto.process_id == process_id:
            return dto
    return None


def get_process_list(process_name_equals: str = None) -> List[ProcessInfoDto]:
    """
    Returns a list of ProcessInfoDto objects
    :param process_name_equals: process name
    :return: List of ProcessInfoDto objects
    """
    if process_name_equals is None:
        return get_process_list("")

    proc_list: List[ProcessInfoDto] = []
    try:
        for proc in psutil.process_iter():
            process_name = proc.name()
            process_id = proc.pid
            if string_helper.is_null_or_empty(process_name_equals) or process_name_equals == process_name:
                process = ProcessInfoDto(process_name, process_id)
                proc_list.append(process)
    except (KeyError, TypeError, ValueError) as ex:
        logging.error("An error occurred while accessing the process.")
        logging.error(ex)
    return proc_list


def get_total_cores() -> int:
    """
    Returns number of total cores of the computer
    :return: number of total cores
    """
    return int(os.cpu_count())


def get_total_memory_in_bytes() -> float:
    """
    Returns total memory bytes.
    :return: total memory bytes
    """
    total_memory_bytes: int = psutil.virtual_memory().total
    return total_memory_bytes


def get_running_process_id() -> str:
    """
    Returns running process id
    :return: running process id
    """
    return str(os.getpid())


def kill_process_by_id(process_id: int):
    """
    Kills process by process id.
    :param process_id: ID of the process
    :return: nothing
    """
    os.kill(process_id, signal.SIGILL)


def get_os_type() -> OsType:
    """
    Returns operating system type id
    :return: operating system type id
    """
    os_type_name: str = platform.system()
    if "WINDOWS" in string_helper.to_upper_eng(os_type_name):
        return OsType.WINDOWS
    if "LINUX" in string_helper.to_upper_eng(os_type_name):
        return OsType.LINUX
    return OsType.NOT_AVAILABLE


def get_working_dir() -> str:
    """
    returns the path of the current working directory
    :return: path of the current working directory
    """
    work_dir = os.getcwd()
    return work_dir
