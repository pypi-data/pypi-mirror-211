"""
This module includes ModelSettings class.
"""

from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class ModelSettings:
    """
    Model settings for supervised feature selection
    """
    ATTR_DICT = {
        "model_params": dict,
        "model_fit_params": dict,
        "reduction_coverage": float
    }

    def __init__(self, **kwargs):
        self.model_params: dict = None
        self.model_fit_params: dict = None
        self.reduction_coverage: float = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
