"""Includes PreprocessingUserInputService class."""

from typing import Union, List

from organon.fl.mathematics.constants import INT_MAX
from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.parameter_helper import USE_CLASS_DEFAULT_STR
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.preprocessing.services.user_settings.coarse_input_dto import CoarseInputDto
from organon.ml.preprocessing.settings.enums.imputer_type import ImputerType
from organon.ml.preprocessing.settings.enums.scaler_type import ScalerType
from organon.ml.preprocessing.settings.objects.coarse_class_settings import CoarseClassSettings
from organon.ml.preprocessing.settings.objects.imputation_settings import ImputationSettings
from organon.ml.preprocessing.settings.objects.one_hot_encoding_settings import OneHotEncodingSettings
from organon.ml.preprocessing.settings.objects.scaling_settings import ScalingSettings


class PreprocessingUserInputService:
    """Service for validating user input and generating settings for preprocessor services"""

    @classmethod
    def get_coarse_class_settings(cls, cc_input: CoarseInputDto) -> CoarseClassSettings:
        """Validates settings entered by user and generates settings object for CoarseClass service"""
        target_type = get_enum(cc_input.target_column_type, TargetType)
        cc_settings = CoarseClassSettings(cc_input.test_ratio,
                                          cc_input.min_class_size, target_type, cc_input.max_leaf_nodes,
                                          cc_input.stability_check,
                                          cc_input.stability_threshold, cc_input.random_state,
                                          cc_input.positive_class, cc_input.negative_class)
        return cc_settings

    @classmethod
    def get_imputation_settings(cls, numeric_data_method: str,
                                categorical_data_method: str = ImputerType.SIMPLE.name,
                                n_strategy: str = USE_CLASS_DEFAULT_STR, c_strategy: str = 'most_frequent',
                                n_missing_values: Union[int, float, None] = USE_CLASS_DEFAULT_STR,
                                c_missing_values: Union[int, float, str, None] = USE_CLASS_DEFAULT_STR,
                                n_fill_value: Union[float, int] = USE_CLASS_DEFAULT_STR,
                                c_fill_value: Union[
                                    str, float, int] = USE_CLASS_DEFAULT_STR,
                                included_columns: List[str] = None) -> ImputationSettings:
        """Validates settings entered by user and generates settings object for Imputation service"""
        # pylint: disable=too-many-arguments
        numeric_imputer_type = get_enum(numeric_data_method, ImputerType)
        categorical_imputer_type = get_enum(categorical_data_method, ImputerType)
        cls._validate_imputation_settings(numeric_imputer_type, categorical_imputer_type, c_strategy)
        return ImputationSettings(numeric_imputer_type, ImputerType.SIMPLE, n_missing_values,
                                  c_missing_values, n_strategy, c_strategy, n_fill_value, c_fill_value,
                                  included_columns)

    @staticmethod
    def _validate_imputation_settings(numeric_imputer_type: ImputerType,
                                      categorical_imputer_type: ImputerType, c_strategy: str):
        if numeric_imputer_type is None:
            raise ValueError("Numeric imputer type is None.")
        if categorical_imputer_type != ImputerType.SIMPLE:
            raise ValueError(
                "The given categorical data imputer cannot be used. Please select SIMPLE as imputer.")
        if c_strategy not in ["most_frequent", "constant"]:
            raise ValueError(
                "The given categorical column imputation strategy cannot be used. "
                "You can select most_frequent or constant strategies.")

    @classmethod
    def get_scaling_settings(cls, strategy: str) -> ScalingSettings:
        """Validates settings entered by user and generates settings object for Scaling service"""
        strategy_type = get_enum(strategy, ScalerType)
        return ScalingSettings(strategy_type)

    @classmethod
    def get_one_hot_encoding_settings(cls, category_cumulative_ratio: float = 1.0,
                                      category_max_number: int = INT_MAX) -> OneHotEncodingSettings:
        """Validates settings entered by user and generates settings object for OneHotEncoding service"""
        return OneHotEncodingSettings(category_cumulative_ratio, category_max_number)
