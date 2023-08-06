"""
This module keeps the functions used in file io operations.
"""
import io
import logging
import os
import pkgutil
from typing import List

from organon.fl.core.fileoperations import directory_helper
from organon.fl.core.fileoperations.file_read_options import FileReadOptions


def read_all_lines(file_read_options: FileReadOptions) -> List[str]:
    """
    Reads the file line by line, and returns a list of strings(lines) of the file.
    :param file_read_options: FileReadOptions object
    :return: a list of strings(lines)
    """
    read_bytes = None
    lines: List[str] = []
    read_str: str
    with io.open(file_read_options.file_full_path, "rb") as read_bytes:
        read_str = read_bytes.readline().decode("utf-8")
        if read_str is None:
            return lines
        read_str = read_str.replace("\uFEFF", "")
        lines.append(read_str)
        read_str = read_bytes.readline().decode("utf-8")
        while read_str != '':
            lines.append(read_str)
            read_str = read_bytes.readline().decode("utf-8")

    return lines


def read_all_text_from_file(path: str) -> str:
    """
    Reads all text of the file.
    :param path: file path
    :return: all text of the file
    """
    with open(path, 'r', encoding="utf8") as file:
        read_file = file.read()
    return read_file


def read_all_text_from_resource_file(resource_name: str) -> str:
    """
    Reads all text of a resource file.
    :param resource_name: file path
    :return: all text of the file
    """
    result: str = ""
    try:
        result = pkgutil.get_data(__name__, resource_name)
    except (ModuleNotFoundError, ValueError, ImportError, NotImplementedError) as ex:
        logging.error("An error occurred while reading the resource file.")
        logging.error(ex)
    return result


def write_to_file(file_path: str, file_detail: str, append: bool = False, ensure_path: bool = False):
    """
    Writes a string to the file.
    :param file_path: file path
    :param file_detail: string to write
    :param append: append to end of file
    :param ensure_path: create path if not exists
    :return:
    """
    mode = "w+b" if not append else "a+b"
    if ensure_path:
        directory_helper.create(get_directory_name(file_path))
    with open(file_path, mode) as out:
        out.write(bytearray(file_detail, 'utf-8'))


def check_file_exists(file_path: str) -> bool:
    """
    Checks if the file exists in the parameter path.
    :param file_path: file path
    :return: bool checks whether the file exists in the parameter path
    """
    return os.path.isfile(file_path) and not os.path.isdir(file_path)


def get_directory_name(file_path: str) -> str:
    """Returns directory name of given file path"""
    return os.path.dirname(file_path)
