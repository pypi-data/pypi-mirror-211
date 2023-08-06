"""This module includes enum class 'DqRecordSourceType'"""
from enum import Enum


class DqRecordSourceType(Enum):
    """
    Types of dq record sources.
    """
    DATABASE = 1
    TEXT = 2
    DATA_FRAME = 3
