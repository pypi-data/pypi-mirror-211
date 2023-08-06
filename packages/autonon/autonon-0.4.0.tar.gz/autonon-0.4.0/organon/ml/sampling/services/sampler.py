"""Includes Sampler class."""
from typing import List

import pandas as pd

from organon.ml.sampling.domain.objects.sampling_output import SamplingOutput
from organon.ml.sampling.domain.services.sampling_service import SamplingService
from organon.ml.sampling.services.user_settings.user_sampling_settings import UserSamplingSettings
from organon.ml.sampling.settings.sampling_user_input_service import SamplingUserInputService


class Sampler:
    """User Interface class for sampling"""

    def __init__(self):
        self._output: SamplingOutput = None

    def execute(self, data: pd.DataFrame, sampling_strategy: str = None, target_column_name: str = None,
                target_type: str = None, strata_columns: List[str] = None, split_test_data: bool = None,
                test_split_ratio: float = None, sampling_ratio: float = None, data_sample_ratio: float = None):
        """todo"""
        # pylint: disable=too-many-arguments
        user_settings = UserSamplingSettings(data, target_column_name, target_type, strata_columns, split_test_data,
                                             test_split_ratio, sampling_strategy, sampling_ratio, data_sample_ratio)
        settings = SamplingUserInputService.get_sampling_settings(user_settings)
        output = SamplingService.sample(settings)
        self._output = output
        return output
