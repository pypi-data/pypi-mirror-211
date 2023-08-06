"""Includes SignalType enum definition."""
from enum import Enum


class SignalType(Enum):
    """Signal types for dq comparisons"""

    GREEN = 1
    YELLOW = 2
    RED = 3
