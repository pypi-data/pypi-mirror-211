"""Includes NullFeatureReductionSettings class."""
from typing import List, Optional
from pandas import DataFrame
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import \
    BaseFeatureReductionSettings


class NullFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for null feature reduction"""

    def __init__(self, data: DataFrame, null_ratio_threshold: float = None,
    excluded_columns: Optional[List[str]] = None):
        super().__init__(data, excluded_columns)
        self.null_ratio_threshold = null_ratio_threshold
