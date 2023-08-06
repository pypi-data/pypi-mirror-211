"""This module includes enum class 'FeatureReductionType'"""
from enum import Enum


class FeatureReductionType(Enum):
    """
    Types of Feature Reduction.
    """
    NULL = 1
    STABILITY = 2
    UNIVARIATE_PERFORMANCE = 3
    SIMILAR_DISTRIBUTION = 4
    HIGH_CORRELATION = 5
