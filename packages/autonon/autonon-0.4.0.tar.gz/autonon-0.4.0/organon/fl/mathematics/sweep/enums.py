"""This module keeps the sweep enumerations."""
from enum import Enum, auto


class RegressionAttributeSelectionMethod(Enum):
    """Enum for regression attribute selection method"""
    STEPWISE = auto()
    FORWARD = auto()
    NONE = auto()


class AttributeSelectionStatus(Enum):
    """Enum for attribute selection status"""
    ENFORCED = auto()
    INCLUDED = auto()
    EXLUDED = auto()
    NEVER_INCLUDED = auto()


class TestStatisticsType(Enum):
    """Enum for test statistics type"""
    F_STATISTICS = auto()
    T_STATISTICS = auto()
    CHI_SQUARE = auto()
