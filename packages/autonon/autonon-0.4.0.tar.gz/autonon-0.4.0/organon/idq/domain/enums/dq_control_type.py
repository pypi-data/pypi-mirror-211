"""Includes DqControlType enum definition."""
from enum import Enum, auto


class DqControlType(Enum):
    """Control types in DQ."""
    EMPTY_TABLE = auto()
    TABLE_COLUMNS = auto()
    STABLE_COLUMN = auto()
    UNEXPECTED_NUMERICAL_VALUES = auto()
    UNEXPECTED_NOMINAL_VALUES = auto()
    DUPLICATE_KEYS = auto()
    COLUMN_MEAN = auto()
    DATA_SOURCE_STATS_TL_CONTROL = auto()
    DATA_SOURCE_STATS_TIME_SERIES_CONTROL = auto()
    PSI_NOMINAL_VALUES = auto()
    PSI_NUMERIC_VALUES = auto()
