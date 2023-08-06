"""
This module includes AfeSupervisedAlgorithmSettings class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.model_settings import ModelSettings


class AfeSupervisedAlgorithmSettings(AfeAlgorithmSettings):
    """
    Algorithm settings for Automated Feature Extraction with Supervised Learning type
    """

    ATTR_DICT = {
        "training_percentage": float,
        "min_data_in_leaf_and_sample_size_control_ratio": float,
        "model_settings": ModelSettings,
        "final_model_settings": ModelSettings
    }
    ATTR_DICT.update(AfeAlgorithmSettings.ATTR_DICT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.training_percentage: float = None
        self.min_data_in_leaf_and_sample_size_control_ratio: float = None

        self.model_settings: ModelSettings = None
        self.final_model_settings: ModelSettings = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
