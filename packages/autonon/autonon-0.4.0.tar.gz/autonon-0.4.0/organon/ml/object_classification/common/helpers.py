"""Includes helpers for object classification"""
from organon.fl.core.fileoperations import directory_helper
from organon.fl.logging.helpers.log_helper import LogHelper


def check_directory(directory: str):
    """Checks if given directory exists"""
    if not directory_helper.exists(directory):
        throw_val_ex_with_log(f"Directory: {directory} not found!")


def throw_val_ex_with_log(msg: str):
    """Raises and logs a value error """
    LogHelper.error(msg)
    raise ValueError(msg)
