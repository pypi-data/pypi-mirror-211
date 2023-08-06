"""Includes FeatureReduction class."""
from typing import List

import pandas as pd

from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput

from organon.ml.feature_reduction.domain.services.feature_reduction_service import FeatureReductionService
from organon.ml.feature_reduction.settings.feature_reduction_user_input_service import FeatureReductionUserInputService
from organon.ml.feature_reduction.settings.objects.user_feature_reduction_settings import UserFeatureReductionSettings

class FeatureReduction:
    """Feature reduction user interface class"""

    def __init__(self):
        self._output: List[FeatureReductionOutput] = None
        self._input_service = FeatureReductionUserInputService()
        self.settings: UserFeatureReductionSettings = UserFeatureReductionSettings()

    def execute(self, data: pd.DataFrame, drop_cols: bool, included_reduction_types: List[str] = None,
                target_type: str = None, target_column_name: str = None, performance_metric: str = None,
                excluded_columns: List[str] = None
                ) -> \
            List[FeatureReductionOutput]:
        """
        Execute feature reduction with given parameters
        :param included_reduction_types:
        :param data:
        :param drop_cols:
        :param target_type:
        :param target_column_name:
        :param performance_metric:
        :return:
        """
        # pylint: disable=too-many-arguments
        self.settings.data = data
        self.settings.included_reduction_types = included_reduction_types
        self.settings.target_type = target_type
        self.settings.target_column_name = target_column_name
        self.settings.performance_metric = performance_metric
        self.settings.excluded_columns = excluded_columns
        feature_reduction_settings = self._input_service.generate_feature_reduction_settings(self.settings)
        self._output = FeatureReductionService.execute(feature_reduction_settings, self.settings.data, drop_cols)

        return self._output

    def set_null_feature_reduction_settings(self, null_ratio_threshold: float = 0.99):
        """
        Set null_ratio_threshold parameter for null feature reduction entered by user
        :param null_ratio_threshold:
        :return:
        """
        self.settings.null_ratio_threshold = null_ratio_threshold

    def set_high_correlated_feature_reduction_settings(self, correlation_threshold: float = 0.99,
                                                       random_state=None):
        """
        Set correlation_threshold parameter for high correlated feature reduction
        :param correlation_threshold:
        :param random_state:
        :return:
        """
        self.settings.correlation_threshold = correlation_threshold
        self.settings.random_state = random_state

    def set_univariate_performance_feature_reduction_settings(self, univariate_performance_threshold: float = None,
                                                              random_state=None):
        """
        Set univariate_performance_threshold parameter for univariate performance feature reduction
        :param univariate_performance_threshold:
        :param random_state:
        :return:
        """
        self.settings.univariate_performance_threshold = univariate_performance_threshold
        self.settings.random_state = random_state

    def set_similar_distribution_feature_reduction_settings(self, nunique_count: int = 20, random_state=None):
        """
        Set nunique_count parameter for similar distribution feature reduction

        :param nunique_count:
        :param random_state:
        :return:
        """
        self.settings.nunique_count = nunique_count
        self.settings.random_state = random_state
