"""Includes SamplingStrategy enum."""
from enum import Enum


class SamplingStrategy(Enum):
    """Sampling Strategy types"""
    OVERSAMPLING = 1
    UNDERSAMPLING = 2
    RANDOM_SAMPLING = 3
