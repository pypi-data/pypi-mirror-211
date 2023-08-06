"""Includes ModelType enum class"""
from enum import Enum, auto


class MapMetrics(Enum):
    """Ultralytics model types"""

    MAP50 = auto()
    MAP75 = auto()
    MAP = auto()
