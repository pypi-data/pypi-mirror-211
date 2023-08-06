"""Includes Preprocessor class."""

from typing import Union, List

from organon.fl.mathematics.constants import INT_MAX
from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.parameter_helper import USE_CLASS_DEFAULT_STR
from organon.ml.preprocessing.domain.services.coarse_class_service import CoarseClassService
from organon.ml.preprocessing.domain.services.imputation_service import ImputationService
from organon.ml.preprocessing.domain.services.one_hot_encoding_service import OneHotEncodingService
from organon.ml.preprocessing.domain.services.scaling_service import ScalingService
from organon.ml.preprocessing.services.user_settings.coarse_input_dto import CoarseInputDto
from organon.ml.preprocessing.settings.enums.imputer_type import ImputerType
from organon.ml.preprocessing.settings.preprocessing_user_input_service import PreprocessingUserInputService


class Preprocessor:
    """User interface class for preprocessing module"""

    @staticmethod
    def get_coarse_class_service(test_ratio: float, target_column_type: str = TargetType.BINARY.name,
                                 min_class_size: int = 1, max_leaf_nodes: int = 20,
                                 stability_check: bool = True,
                                 stability_threshold: float = 0.30, random_state=42,
                                 positive_class: str = None, negative_class: str = None) -> CoarseClassService:
        """returns coarse class service"""
        # pylint: disable=too-many-arguments
        cc_input = CoarseInputDto(test_ratio, target_column_type, min_class_size, max_leaf_nodes, stability_check,
                                  stability_threshold, random_state, positive_class, negative_class)
        cc_settings = PreprocessingUserInputService.get_coarse_class_settings(cc_input)
        return CoarseClassService(cc_settings)

    @staticmethod
    def get_imputation_service(numeric_data_method: str,
                               categorical_data_method: str = ImputerType.SIMPLE.name,
                               n_missing_values: Union[int, float] = USE_CLASS_DEFAULT_STR,
                               c_missing_values: Union[int, float, str] = USE_CLASS_DEFAULT_STR,
                               n_fill_value: Union[float, int] = USE_CLASS_DEFAULT_STR,
                               c_fill_value: Union[str, float, int] = USE_CLASS_DEFAULT_STR,
                               n_strategy: str = USE_CLASS_DEFAULT_STR,
                               c_strategy: str = 'most_frequent',
                               included_columns: List[str] = None) -> ImputationService:
        """
        returns imputation service with given parameters.

        :param data: train data used to fit imputer.
        :param numeric_data_method: type of imputer for numeric columns, "SIMPLE" or "ITERATIVE".
        :param categorical_data_method: type of imputer for categorical columns.
            default: "SIMPLE".
        :param n_missing_values: used to fill numerical imputer missing_values field.
            default: imputer default if None given.
        :param c_missing_values: used to fill categorical imputer missing_values field.
            default: imputer default if None given.
        :param n_fill_value: used to fill numerical imputer fill_value field.
            default: imputer default if None given.
        :param c_fill_value: used to fill categorical imputer fill_value field.
            default: imputer default if None given.
        :param n_strategy: used to fill numerical imputer strategy field.
            default: imputer default if None given.
        :param c_strategy: used to fill categorical imputer strategy field.
            default: "most-frequent"
        :param included_columns: columns to impute
            default: "all columns"
        """
        # pylint: disable=too-many-arguments
        imputation_settings = PreprocessingUserInputService.get_imputation_settings(numeric_data_method,
                                                                                    categorical_data_method,
                                                                                    n_strategy, c_strategy,
                                                                                    n_missing_values, c_missing_values,
                                                                                    n_fill_value, c_fill_value,
                                                                                    included_columns)
        return ImputationService(imputation_settings)

    @staticmethod
    def get_one_hot_encoding_service(category_cumulative_ratio: float = 1.0, category_max_number: int = INT_MAX):
        """
        Returns one hot encoding service with given parameter settings.

        :param float category_cumulative_ratio: cumulative percentage of categories that will be taken as a feature,
        default: 1.0
        :param int category_max_number: maximum number of features to restrict produced features by threshold,
        default: infinite
        """
        one_hot_settings = PreprocessingUserInputService.get_one_hot_encoding_settings(category_cumulative_ratio,
                                                                                       category_max_number)
        service = OneHotEncodingService(one_hot_settings)
        return service

    @staticmethod
    def get_scaling_service(strategy: str):
        """Returns service for scaling numerical columns"""
        scaling_settings = PreprocessingUserInputService.get_scaling_settings(strategy)
        return ScalingService(scaling_settings)
