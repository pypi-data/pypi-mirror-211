"""Includes FeatureReductionOutput class"""
from typing import List

from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType


class FeatureReductionOutput:
    """Output of feature reduction"""

    def __init__(self):
        self.feature_reduction_type: FeatureReductionType = None
        self.reduced_column_list: List[str] = None
