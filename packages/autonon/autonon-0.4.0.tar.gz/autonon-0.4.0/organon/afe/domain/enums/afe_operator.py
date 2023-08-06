"""
This module includes enum class AfeOperator.
"""
from enum import Enum
from typing import List


# pylint: disable=invalid-name
class AfeOperator(Enum):
    """
    Operators for AFE calculations
    """
    Density = 0
    Min = 1
    Max = 2
    Sum = 3
    Frequency = 4
    TimeSinceFirst = 5
    TimeSinceLast = 6
    Ratio = 7
    SumTrend = 8
    FrequencyTrend = 9
    DensityTrend = 10
    CountDistinct = 11
    Mode = 12


OPERATOR_SET_ONE: List[AfeOperator] = [AfeOperator.Density, AfeOperator.Sum, AfeOperator.Max,
                                       AfeOperator.Min, AfeOperator.Frequency, AfeOperator.CountDistinct,
                                       AfeOperator.Mode]
OPERATOR_SET_TWO: List[AfeOperator] = [AfeOperator.TimeSinceFirst, AfeOperator.TimeSinceLast]
OPERATOR_SET_THREE: List[AfeOperator] = [AfeOperator.SumTrend, AfeOperator.DensityTrend,
                                         AfeOperator.FrequencyTrend]
