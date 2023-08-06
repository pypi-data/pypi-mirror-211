"""
This module includes enum class AfeTargetColumnType.
"""
from enum import Enum


# pylint: disable=invalid-name
class AfeTargetColumnType(Enum):
    """
    AfeTargetColumnType
    """
    Binary = 0
    Scalar = 1
    MultiClass = 3
