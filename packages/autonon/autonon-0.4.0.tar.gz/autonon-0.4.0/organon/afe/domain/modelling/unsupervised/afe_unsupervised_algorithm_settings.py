"""
This module includes AfeUnsupervisedAlgorithmSettings class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings


class AfeUnsupervisedAlgorithmSettings(AfeAlgorithmSettings):
    """
    Algorithm settings for Automated Feature Extraction with Unsupervised Learning type
    """
    ATTR_DICT = {
        "bin_count": int,
        "r_factor": float,
        "random_state": int,
        "max_column_count": int,
        "is_logging": bool
    }
    ATTR_DICT.update(AfeAlgorithmSettings.ATTR_DICT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bin_count: int = None
        self.r_factor: float = None
        self.random_state: int = None
        self.max_column_count: int = None
        self.is_logging: bool = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
