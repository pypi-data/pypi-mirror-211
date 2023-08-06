"""
This module DateIntervalType enum class.
"""
from enum import Enum


class DateIntervalType(Enum):
    """
    Enum class for defining date interval type values.
    """
    OPEN_OPEN = 0
    OPEN_CLOSED = 1
    CLOSED_OPEN = 2
    CLOSED_CLOSED = 3
