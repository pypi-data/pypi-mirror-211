"""Includes ModellerType enum class."""
from enum import auto, Enum


class ModellerType(Enum):
    """Modeller Types"""
    CLASSIFIER = auto()
    REGRESSOR = auto
