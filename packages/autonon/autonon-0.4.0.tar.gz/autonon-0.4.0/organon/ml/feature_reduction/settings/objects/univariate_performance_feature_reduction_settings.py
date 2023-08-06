"""Includes UnivariatePerformanceFeatureReductionSettings class."""
from typing import Optional, List
from pandas import DataFrame
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings

class UnivariatePerformanceFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for univariate performance feature reduction"""

    def __init__(self, data: DataFrame, target_type: TargetType = None,
                 target_column_name: str = None,
                 performance_metric: str = None,
                 univariate_performance_threshold: float = None,
                 random_state: int = None, excluded_columns: Optional[List[str]] = None):
        # pylint: disable=too-many-arguments
        super().__init__(data, excluded_columns)
        self.target_type: TargetType = target_type
        self.target_column_name: str = target_column_name
        self.performance_metric: str = performance_metric
        self.univariate_performance_threshold: float = univariate_performance_threshold
        self.random_state: int = random_state
