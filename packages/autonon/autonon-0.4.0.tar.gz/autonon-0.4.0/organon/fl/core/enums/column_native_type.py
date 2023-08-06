"""
This module ColumnNativeType enum class.
"""
from enum import Enum


# pylint: disable=invalid-name
class ColumnNativeType(Enum):
    """
    Enum class for defining column native type values.
    """
    String = 1
    Numeric = 2
    Other = 3
    Date = 4
