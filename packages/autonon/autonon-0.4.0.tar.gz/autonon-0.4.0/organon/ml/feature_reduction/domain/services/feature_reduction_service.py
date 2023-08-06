"""Includes FeatureReductionService class"""
from typing import List, Dict

import pandas as pd

from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.objects.high_corr_reduction_output import HighCorrReductionOutput
from organon.ml.feature_reduction.domain.objects.similar_dist_reduction_output import SimilarDistReductionOutput
from organon.ml.feature_reduction.domain.objects.univariate_performance_reduction_output import \
    UnivariatePerformanceFeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.high_correlated_feature_reduction import \
    HighCorrelatedFeatureReduction
from organon.ml.feature_reduction.domain.reductions.null_feature_reduction import NullFeatureReduction
from organon.ml.feature_reduction.domain.reductions.similar_distribution_feature_reduction import \
    SimilarDistributionFeatureReduction
from organon.ml.feature_reduction.domain.reductions.stability_feature_reduction import StabilityFeatureReduction
from organon.ml.feature_reduction.domain.reductions.univariate_performance_feature_reduction import \
    UnivariatePerformanceFeatureReduction
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.high_correlated_feature_reduction_settings import \
    HighCorrelatedFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.null_feature_reduction_settings import NullFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.similar_distribution_feature_reduction_settings import \
    SimilarDistributionFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.stability_feature_reduction_settings import \
    StabilityFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.univariate_performance_feature_reduction_settings import \
    UnivariatePerformanceFeatureReductionSettings


class FeatureReductionService:
    """Domain service for feature reduction"""

    @classmethod
    def get_reduction_classes_ordered(cls):
        """Returns all control classes for executor
        """
        # NOTE: Please do not change dict order. Because order is important!
        feature_reduction_dict = {
            NullFeatureReductionSettings: NullFeatureReduction,
            StabilityFeatureReductionSettings: StabilityFeatureReduction,
            UnivariatePerformanceFeatureReductionSettings: UnivariatePerformanceFeatureReduction,
            SimilarDistributionFeatureReductionSettings: SimilarDistributionFeatureReduction,
            HighCorrelatedFeatureReductionSettings: HighCorrelatedFeatureReduction
        }
        return feature_reduction_dict

    @classmethod
    def execute(cls, settings: List[BaseFeatureReductionSettings], data: pd.DataFrame, drop_cols: bool) -> List[
        FeatureReductionOutput]:
        """
        Executes feature reduction with given feature reduction type and settings.
        :param settings:
        :param data:
        :param drop_cols:
        :return:
        """
        feature_reduction_dict = cls.get_reduction_classes_ordered()
        result_list: List[FeatureReductionOutput] = []
        column_univariate_performances: Dict[str, float] = {}
        for feature_reduction_settings, feature_reduction_settings_service in feature_reduction_dict.items():
            for setting in settings:
                if isinstance(setting, feature_reduction_settings):
                    if isinstance(setting, SimilarDistributionFeatureReductionSettings):
                        setting.univariate_performance_result = column_univariate_performances
                    if isinstance(setting, HighCorrelatedFeatureReductionSettings):
                        setting.univariate_performance_result = column_univariate_performances
                    result = feature_reduction_settings_service(setting).execute()
                    res_columns = result.reduced_column_list
                    result_list.append(result)

                    if isinstance(result, UnivariatePerformanceFeatureReductionOutput):
                        column_univariate_performances.update(result.univariate_performance_result)
                    elif isinstance(result, SimilarDistReductionOutput):
                        if result.new_univariate_performance_results is not None:
                            column_univariate_performances.update(result.new_univariate_performance_results)
                    elif isinstance(result, HighCorrReductionOutput):
                        if result.new_univariate_performance_results is not None:
                            column_univariate_performances.update(result.new_univariate_performance_results)

                    if drop_cols and res_columns is not None:
                        data.drop(res_columns, axis=1, inplace=True)

            if len(data.columns) == 0:
                return result_list

        return result_list
