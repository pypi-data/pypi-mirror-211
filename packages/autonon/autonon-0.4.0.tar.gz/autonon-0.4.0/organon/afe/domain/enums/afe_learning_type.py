"""
This module includes enum class AfeLearningType.
"""
from enum import Enum


# pylint: disable=invalid-name
class AfeLearningType(Enum):
    """
    Learning type for Automated Feature Extraction
    """
    Supervised = 0
    Unsupervised = 1
