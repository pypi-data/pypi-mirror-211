"""Includes RandomFlipType enum class"""
from enum import Enum, auto


class RandomFlipType(Enum):
    """Random flip types"""
    VERTICAL = auto()
    HORIZONTAL = auto()
    HORIZONTAL_AND_VERTICAL = auto()
    