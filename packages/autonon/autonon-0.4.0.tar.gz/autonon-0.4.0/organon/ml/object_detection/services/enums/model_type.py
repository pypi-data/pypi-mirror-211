"""Includes ModelType enum class"""
from enum import Enum, auto


class ModelTypes(Enum):
    """Ultralytics model types"""

    NANO = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    XLARGE = auto()
