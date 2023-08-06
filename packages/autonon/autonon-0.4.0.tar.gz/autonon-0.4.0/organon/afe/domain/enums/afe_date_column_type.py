"""
This module includes enum class AfeDateColumnType.
"""
from enum import Enum


# pylint: disable=invalid-name
class AfeDateColumnType(Enum):
    """
    AfeDateColumnType
    """
    YyyyMmDd = 0
    YyyyMm = 1
    DateTime = 2
    CustomFormat = 3
