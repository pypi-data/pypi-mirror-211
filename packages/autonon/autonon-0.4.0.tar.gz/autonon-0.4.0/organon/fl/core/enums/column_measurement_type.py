"""
This module keeps ColumnMeasurementType enum class.
"""
from enum import Enum


class ColumnMeasurementType(Enum):
    """
    Enum class for defining column measurement type values.
    """
    NOT_ASSIGNED = 0
    NOMINAL = 1
    NUMERIC = 2
    OTHER = 3
    DATE = 4
