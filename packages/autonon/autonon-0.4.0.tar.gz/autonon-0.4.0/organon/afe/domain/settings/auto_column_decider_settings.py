"""
This module includes AutoColumnDeciderSettings class.
"""
from typing import List

from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class AutoColumnDeciderSettings:
    """
    Class for parameters about the AutoColumnDeciderService
    """
    ATTR_DICT = {
        "sampling_ratio": float,
        "numeric_to_dimension": int,
        "dimension_distinct_cut_off": float,
        "use_dimension_columns": bool,
        "rejected_dimension_columns": List[str],
        "use_quantity_columns": bool,
        "rejected_quantity_columns": List[str]
    }

    def __init__(self, **kwargs):
        self.sampling_ratio: float = None
        self.numeric_to_dimension: int = None
        self.dimension_distinct_cut_off: float = None
        self.use_dimension_columns: bool = None
        self.rejected_dimension_columns: List[str] = None
        self.use_quantity_columns: bool = None
        self.rejected_quantity_columns: List[str] = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
