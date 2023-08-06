"""Includes ColorType enum class"""
from enum import Enum, auto


class ColorType(Enum):
    """Color types"""
    RGB = auto()
    RGBA = auto()
    GRAY = auto()
    