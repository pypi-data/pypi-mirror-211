"""Includes SearchType enum class."""
from enum import Enum, auto


class SearchType(Enum):
    """Search types for hyperparameter optimization"""
    GRID = auto()
    RANDOM = auto()
    MODEL_BASED = auto()
