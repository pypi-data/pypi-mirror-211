"""
This module includes enum class TargetType.
"""
from enum import Enum


class TargetType(Enum):
    """
    TargetType
    """
    BINARY = 1
    SCALAR = 2
    MULTICLASS = 3
