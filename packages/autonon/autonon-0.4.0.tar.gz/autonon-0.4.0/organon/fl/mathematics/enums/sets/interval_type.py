"""
This module includes IntervalType enum definition.
"""
from enum import Enum


class IntervalType(Enum):
    """IntervalType enum class"""
    OPEN_OPEN = 0
    OPEN_CLOSED = 1
    CLOSED_OPEN = 2
    CLOSED_CLOSED = 3
