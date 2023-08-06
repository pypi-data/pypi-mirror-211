"""
This module includes enum class BinaryTargetClass.
"""
from enum import Enum


# pylint: disable=invalid-name
class BinaryTargetClass(Enum):
    """
    BinaryTargetClass
    """
    NAN = -1
    POSITIVE = 0
    NEGATIVE = 1
    EXCLUSION = 2
    INDETERMINATE = 3
