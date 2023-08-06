"""
This module keeps the get_current_directory function.
"""
import os
import shutil
from typing import List


def get_current_directory() -> str:
    """
    Returns the current working directory path.
    :return: current working directory path
    """
    path = os.getcwd()
    return path


def get_name(path: str) -> str:
    """
    Returns the name of the file in the given path
    :return: name of the file in the given path
    """
    return os.path.basename(path)


def exists(path: str) -> bool:
    """
    Returns True if given path exists
    """
    return os.path.isdir(path)


def create(path: str, exception_if_exists: bool = False):
    """
    Creates directories and subdirectories for given path
    """
    os.makedirs(path, exist_ok=not exception_if_exists)


def copy_files(file_paths: List[str], target_dir: str):
    """Copies given files to target directory"""
    create(target_dir, exception_if_exists=False)
    for file in file_paths:
        shutil.copy(file, os.path.join(target_dir, os.path.basename(file)))


def copy_dir(source_dir: str, target_dir: str):
    """Copies given directory to target directory"""
    shutil.copytree(source_dir, target_dir)


def delete_directory_with_contents(directory: str, ignore_errors: bool = False):
    """Deletes directory and all its contents"""
    shutil.rmtree(directory, ignore_errors)
