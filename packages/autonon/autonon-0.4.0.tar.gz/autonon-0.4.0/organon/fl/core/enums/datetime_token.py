"""Includes DatetimeToken enum class."""
from enum import Enum


class DatetimeToken(Enum):
    """Datetime tokens"""
    NOT_AVAILABLE = 0
    MILLISECOND = 1
    SECOND = 2
    MINUTE = 3
    HOUR = 4
    DAY = 5
    MONTH = 6
    YEAR = 7
