""" This module includes UnivariatePerformanceFeatureReduction"""
from typing import List

from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.helpers.univariate_performance_helper import \
    get_univariate_performances_for_columns
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.objects.univariate_performance_reduction_output import \
    UnivariatePerformanceFeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.univariate_performance_feature_reduction_settings import \
    UnivariatePerformanceFeatureReductionSettings


class UnivariatePerformanceFeatureReduction(BaseFeatureReduction):
    """UnivariatePerformanceFeatureReduction class"""

    def _execute_reduction(self, settings: UnivariatePerformanceFeatureReductionSettings) -> FeatureReductionOutput:
        included_columns = self._get_included_columns(settings.data, settings.excluded_columns)
        if settings.target_column_name in included_columns:
            included_columns.remove(settings.target_column_name)

        scores = get_univariate_performances_for_columns(
            settings.data, included_columns,
            settings.target_column_name, settings.target_type, settings.performance_metric,
            settings.random_state
        )
        if len(scores) == 0:
            reduced_columns = None
        else:
            reduced_columns = [col for col, score in scores.items()
                               if score is not None and score < settings.univariate_performance_threshold]
        output = UnivariatePerformanceFeatureReduction._get_output(reduced_columns, scores)
        return output

    @staticmethod
    def _get_output(reduced_columns: List[str], score_result) -> UnivariatePerformanceFeatureReductionOutput:
        """
        Get output for univariate performance feature reduction.
        Parameters
        ----------
        reduced_columns
        score_result

        Returns
        -------
        Returns UnivariatePerformanceFeatureReductionOutput
        """
        output = UnivariatePerformanceFeatureReductionOutput()
        output.feature_reduction_type = FeatureReductionType.UNIVARIATE_PERFORMANCE
        output.reduced_column_list = reduced_columns
        output.univariate_performance_result = score_result
        return output

    def get_description(self) -> str:
        return "Univariate Performance Feature Reduction"
