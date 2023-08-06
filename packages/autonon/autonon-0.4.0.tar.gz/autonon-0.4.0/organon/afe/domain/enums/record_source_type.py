"""This module includes enum class 'RecordSourceType'"""
from enum import Enum


class RecordSourceType(Enum):
    """
    Types of record sources.
    """
    DATABASE = 1
    TEXT = 2
    DATA_FRAME = 3
