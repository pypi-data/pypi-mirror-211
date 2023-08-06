"""Includes HighCorrelatedFeatureReductionSettings class."""
from typing import Dict, Optional, List
from pandas import DataFrame
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings

class HighCorrelatedFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for high correlated feature reduction"""
    def __init__(self, data: DataFrame, target_type: TargetType = None,
                 target_column_name: str = None,
                 performance_metric: str = None,
                 correlation_threshold: float = None,
                 univariate_performance_result: Optional[Dict[str, float]] = None,
                 random_state: int = None, excluded_columns: Optional[List[str]] = None):
        # pylint: disable=too-many-arguments
        super().__init__(data, excluded_columns)
        self.target_type: TargetType = target_type
        self.target_column_name: str = target_column_name
        self.performance_metric: str = performance_metric
        self.correlation_threshold: float = correlation_threshold
        self.univariate_performance_result: Optional[Dict[str, float]] = univariate_performance_result
        self.random_state: int = random_state
