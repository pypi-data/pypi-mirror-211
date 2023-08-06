"""Includes DqTaskType"""
from enum import Enum


class DqTaskType(Enum):
    """DQ task types"""
    CALCULATION_TABLE_STATS = 1
    CALCULATION_SAMPLE_STATS = 2
    CALCULATION_NOMINAL_STATS = 3
    CALCULATION_NUMERICAL_STATS = 4
    COMPARISON = 5
