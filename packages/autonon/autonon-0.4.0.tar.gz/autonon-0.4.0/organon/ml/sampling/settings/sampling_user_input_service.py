"""Includes SamplingUserInputService class."""

from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.user_input_service_helper import get_enum, get_default_if_none
from organon.ml.sampling.services.user_settings.user_sampling_settings import UserSamplingSettings
from organon.ml.sampling.settings.enums.sampling_strategy import SamplingStrategy
from organon.ml.sampling.settings.objects.sampling_settings import SamplingSettings


class SamplingUserInputService:
    """Service for validating user input and generating settings for sampling"""

    @classmethod
    def get_sampling_settings(cls, user_settings: UserSamplingSettings) -> SamplingSettings:
        """Validates settings entered by user and generates settings object"""
        target_type = get_enum(user_settings.target_type, TargetType)
        sampling_strategy = get_enum(user_settings.sampling_strategy, SamplingStrategy)
        strata_columns = get_default_if_none(user_settings.strata_columns, [])

        if user_settings.data is None:
            raise ValueError("Data to sample should be given")
        if user_settings.target_column_name is not None:
            if len(strata_columns) == 0:
                strata_columns.append(user_settings.target_column_name)
            if target_type is None:
                raise ValueError("Type of target column should be given.")

        if sampling_strategy in [SamplingStrategy.OVERSAMPLING, SamplingStrategy.UNDERSAMPLING]:
            if user_settings.target_column_name is None or \
                    target_type not in [TargetType.BINARY, TargetType.MULTICLASS]:
                raise ValueError("Oversampling and undersampling can only be used when there is a binary or multiclass "
                                 "target column")
            if target_type == TargetType.MULTICLASS and user_settings.sampling_ratio is not None:
                raise ValueError("Sampling ratio cannot be used for undersampling or oversampling with multiclass "
                                 "target")

        split_test_data = get_default_if_none(user_settings.split_test_data, True)
        test_split_ratio = get_default_if_none(user_settings.test_split_ratio, 0.3)
        sampling_ratio = get_default_if_none(user_settings.sampling_ratio, 0.5)

        return SamplingSettings(user_settings.data, user_settings.target_column_name, target_type, strata_columns,
                                split_test_data, test_split_ratio, sampling_strategy, sampling_ratio,
                                user_settings.data_sample_ratio)
