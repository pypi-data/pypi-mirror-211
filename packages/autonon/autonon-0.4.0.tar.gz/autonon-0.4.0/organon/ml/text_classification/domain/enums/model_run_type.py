"""Includes ModelRunType enum class"""
from enum import Enum, auto


class ModelRunType(Enum):
    """Running mode type enums"""
    HIGH_PERFORMANCE = auto()
    EFFICIENT = auto()
