"""Includes FeatureReductionUserInputService class."""
from typing import List

import pandas as pd
from organon.ml.common.helpers.user_input_service_helper import get_default_if_none, get_enum
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
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
from organon.ml.feature_reduction.settings.objects.user_feature_reduction_settings import UserFeatureReductionSettings

class FeatureReductionUserInputService:
    """Service for validating user input and generating settings for feature reduction"""

    @staticmethod
    def _set_default_metric(value: str, target_type: TargetType) -> str:
        """
        Set default metric
        :param value:
        :param target_type:
        :return:
        """
        if value is not None:
            return value
        if target_type.name == TargetType.BINARY.name:
            return "roc_auc"
        if target_type.name == TargetType.MULTICLASS.name:
            return "roc_auc_ovr_weighted"
        if target_type.name == TargetType.SCALAR.name:
            return "r2"
        raise KnownException("Please control target type.")

    @staticmethod
    def _set_default_univariate_performance_threshold(value: float, target_type: TargetType) -> float:
        """Set default univariate performance threshold"""
        if value is not None:
            return value
        if target_type.name == TargetType.BINARY.name:
            return 0.55
        if target_type.name == TargetType.MULTICLASS.name:
            return 0.55
        if target_type.name == TargetType.SCALAR.name:
            return 0.05
        raise KnownException("Please control target type.")

    @staticmethod
    def _get_included_reduction_types(input_settings: UserFeatureReductionSettings) -> List[str]:
        """
        Return included_reduction_types
        :param input_settings:
        :return:
        """
        included_reduction_types = input_settings.included_reduction_types
        if included_reduction_types is None:
            included_reduction_types_list = [FeatureReductionType.NULL.name,
                                             FeatureReductionType.STABILITY.name,
                                             FeatureReductionType.UNIVARIATE_PERFORMANCE.name,
                                             FeatureReductionType.SIMILAR_DISTRIBUTION.name,
                                             FeatureReductionType.HIGH_CORRELATION.name
                                             ]
            if input_settings.target_column_name is None:
                included_reduction_types_list.remove(FeatureReductionType.UNIVARIATE_PERFORMANCE.name)
        else:
            included_reduction_types_list = included_reduction_types
        return included_reduction_types_list

    def generate_feature_reduction_settings(self, input_settings: UserFeatureReductionSettings) -> List[
        BaseFeatureReductionSettings]:

        """
        Generate Feature Reduction Settings list
        :return:
        """
        settings = []
        if input_settings.target_column_name is not None:
            excluded_column_names = input_settings.excluded_columns + [
                input_settings.target_column_name] if input_settings.excluded_columns is not None else [
                input_settings.target_column_name]
        else:
            excluded_column_names = input_settings.excluded_columns
        included_reduction_types = self._get_included_reduction_types(input_settings)

        if FeatureReductionType.NULL.name in included_reduction_types:
            settings.append(self.get_null_feature_reduction_settings(
                input_settings.data, input_settings.null_ratio_threshold, excluded_column_names))

        if FeatureReductionType.STABILITY.name in included_reduction_types:
            settings.append(
                self.get_stability_feature_reduction_settings(input_settings.data, excluded_column_names))

        if FeatureReductionType.UNIVARIATE_PERFORMANCE.name in included_reduction_types:
            settings.append(self.get_univariate_performance_feature_reduction_settings(
                input_settings.data, input_settings.target_type, input_settings.target_column_name,
                input_settings.performance_metric, input_settings.univariate_performance_threshold,
                input_settings.random_state, excluded_column_names))

        if FeatureReductionType.SIMILAR_DISTRIBUTION.name in included_reduction_types:
            settings.append(self.get_similar_distribution_feature_reduction_settings(
                input_settings.data, input_settings.target_type, input_settings.target_column_name,
                input_settings.performance_metric, input_settings.nunique_count,
                input_settings.random_state, excluded_column_names))

        if FeatureReductionType.HIGH_CORRELATION.name in included_reduction_types:
            settings.append(self.get_high_correlated_feature_reduction_settings(
                input_settings.data, input_settings.target_type, input_settings.target_column_name,
                input_settings.performance_metric, input_settings.correlation_threshold,
                input_settings.random_state, excluded_column_names))

        return settings

    @classmethod
    def get_stability_feature_reduction_settings(cls, data: pd.DataFrame, excluded_col_names: List[
        str] = None) -> StabilityFeatureReductionSettings:
        """
        Validates settings for stability feature reduction entered by user and generates settings object
        :param data:
        :param excluded_col_names:
        :return:
        """
        if data is None:
            raise ValueError("Data should be given")
        return StabilityFeatureReductionSettings(data, excluded_columns=excluded_col_names)

    @classmethod
    def get_null_feature_reduction_settings(cls, data: pd.DataFrame, null_ratio_threshold: float = None,
                                            excluded_col_names: List[str] = None) -> NullFeatureReductionSettings:
        """
        Validates settings for null feature reduction entered by user and generates settings object
        :param data:
        :param null_ratio_threshold:
        :param excluded_col_names:
        :return:
        """
        if data is None:
            raise ValueError("Data should be given")
        null_ratio_threshold = get_default_if_none(null_ratio_threshold, 0.99)
        return NullFeatureReductionSettings(data, null_ratio_threshold, excluded_columns=excluded_col_names)

    @classmethod
    def get_high_correlated_feature_reduction_settings(cls, data: pd.DataFrame, target_type: str = None,
                                                       target_column_name: str = None, performance_metric: str = None,
                                                       correlation_threshold: float = None,
                                                       random_state=None, excluded_col_names: List[
                str] = None) -> \
            HighCorrelatedFeatureReductionSettings:
        """
        Validates settings for high correlated feature reduction entered by user and generates settings object
        :param data:
        :param target_type:
        :param target_column_name:
        :param performance_metric:
        :param correlation_threshold:
        :param random_state:
        :return:
        """
        # pylint: disable=too-many-arguments
        if data is None:
            raise ValueError("Data should be given")
        correlation_threshold = get_default_if_none(correlation_threshold, 0.99)
        target_type = get_enum(target_type, TargetType)
        if target_column_name is not None:
            if target_type is None:
                raise ValueError("Type of target column should be given.")
            performance_metric = FeatureReductionUserInputService._set_default_metric(performance_metric, target_type)
            random_state = get_default_if_none(random_state, 42)
        return HighCorrelatedFeatureReductionSettings(data, target_type, target_column_name,
                                                      performance_metric,
                                                      correlation_threshold, None, random_state,
                                                      excluded_columns=excluded_col_names)

    @classmethod
    def get_similar_distribution_feature_reduction_settings(cls, data: pd.DataFrame, target_type: str = None,
                                                            target_column_name: str = None,
                                                            performance_metric: str = None,
                                                            nunique_count: int = None,
                                                            random_state=None,
                                                            excluded_col_names: List[str] = None) -> \
            SimilarDistributionFeatureReductionSettings:
        """
        Validates settings for similar distribution feature reduction
        entered by user and generates settings object
        :param data:
        :param target_type:
        :param target_column_name:
        :param performance_metric:
        :param nunique_count:
        :param random_state:
        :return:
        """
        # pylint: disable=too-many-arguments
        if data is None:
            raise ValueError("Data should be given")
        target_type = get_enum(target_type, TargetType)
        nunique_count = get_default_if_none(nunique_count, 20)
        if target_column_name is not None:
            if target_type is None:
                raise ValueError("Type of target column should be given.")
            performance_metric = FeatureReductionUserInputService._set_default_metric(performance_metric, target_type)
            random_state = get_default_if_none(random_state, 42)

        return SimilarDistributionFeatureReductionSettings(data, target_type, target_column_name,
                                                           performance_metric,
                                                           nunique_count, None, random_state,
                                                           excluded_columns=excluded_col_names)

    @classmethod
    def get_univariate_performance_feature_reduction_settings(cls, data: pd.DataFrame, target_type: str,
                                                              target_column_name: str, performance_metric: str = None,
                                                              univariate_performance_threshold: float = None,
                                                              random_state=None, excluded_col_names: List[
                str] = None) -> UnivariatePerformanceFeatureReductionSettings:
        """
        Validates settings for univariate performance feature reduction entered by user and generates settings object
        :param data:
        :param target_type:
        :param target_column_name:
        :param performance_metric:
        :param univariate_performance_threshold:
        :param random_state:
        :return:
        """
        # pylint: disable=too-many-arguments
        if data is None:
            raise ValueError("Data should be given")
        if target_column_name is None or target_type is None:
            raise ValueError("Target column name and type of target column should be given.")
        target_type = get_enum(target_type, TargetType)
        performance_metric = FeatureReductionUserInputService._set_default_metric(performance_metric, target_type)
        random_state = get_default_if_none(random_state, 42)

        univariate_performance_threshold = FeatureReductionUserInputService \
            ._set_default_univariate_performance_threshold(univariate_performance_threshold, target_type)
        return UnivariatePerformanceFeatureReductionSettings(data, target_type, target_column_name,
                                                             performance_metric,
                                                             univariate_performance_threshold, random_state,
                                                             excluded_columns=excluded_col_names)
