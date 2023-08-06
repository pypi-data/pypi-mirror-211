"""
This module includes AfeProcessSettings class.
"""
import numpy as np

from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class AfeProcessSettings:
    """
    Settings for Automated Feature Extraction process
    """
    ATTR_DICT = {
        "process_id": str,
        "number_of_cores": int,
        "max_memory_size": np.float64,
        "max_execution_time_in_seconds": np.int64
    }

    def __init__(self, **kwargs):
        self.process_id: str = None
        self.number_of_cores: int = None
        self.max_memory_size: np.float64 = None
        self.max_execution_time_in_seconds: np.int64 = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
