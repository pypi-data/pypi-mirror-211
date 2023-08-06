"""Includes ClassificationType enum class"""
from enum import Enum, auto


class ClassificationType(Enum):
    """Classification types"""
    BINARY = auto()
    MULTICLASS = auto()
