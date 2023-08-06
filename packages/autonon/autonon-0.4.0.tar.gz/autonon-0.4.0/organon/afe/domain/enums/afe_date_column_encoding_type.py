"""
This module includes enum class AfeDateColumnEncodingType.
"""
from enum import Enum


# pylint: disable=invalid-name
class AfeDateColumnEncodingType(Enum):
    """
    Keeps encoding type for a column.
    Datetime: datetime.datetime type is an example.
    String: a date column can be a string like '20221001'
    Integer: a date column can be a number like 20220101
    """
    DateTime = 0
    String = 1
    Integer = 2
