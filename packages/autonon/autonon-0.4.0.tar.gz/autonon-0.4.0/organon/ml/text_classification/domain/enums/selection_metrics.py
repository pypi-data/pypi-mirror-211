"""Includes SelectionMetrics enum class"""
from enum import Enum, auto


class SelectionMetrics(Enum):
    """Best Model Selection Metrics for Grid Search"""
    VAL_LOSS = auto()
    ROC_AUC = auto()
    ACC_SCORE = auto()
    F1_SCORE = auto()
