"""Class for Run Type Enum"""
from enum import Enum


class DqRunType(Enum):
    """Run type enum"""
    RUN_ONE_DATA_SOURCE = 1
    RUN_ONE_DATA_SOURCE_WITH_PARTITIONS = 2
    RUN_MULTIPLE_DATA_SOURCE = 3
