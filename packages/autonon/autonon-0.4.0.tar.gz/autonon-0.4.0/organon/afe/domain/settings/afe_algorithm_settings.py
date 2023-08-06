"""
This module includes AfeAlgorithmSettings class.
"""

from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class AfeAlgorithmSettings:
    """
    Base class for algorithm settings
    """
    ATTR_DICT = {
        "dimension_compression_ratio": float,
        "dimension_max_cardinality": int
    }

    def __init__(self, **kwargs):
        self.dimension_compression_ratio: float = None
        self.dimension_max_cardinality: int = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
