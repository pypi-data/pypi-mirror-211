"""
This module includes enum class DateResolution.
"""
from enum import Enum


# pylint: disable=invalid-name
class DateResolution(Enum):
    """
    DateResolution
    """
    Year = 0
    Month = 1
    Day = 2
    Hour = 3
    Minute = 4
    Second = 5
