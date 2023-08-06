"""
This module includes TemporalGrid class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class TemporalGrid:
    """
    Class to define a horizon list for AFE algorithm settings
    """
    ATTR_DICT = {
        "length": int,
        "stride": int,
        "offset": int
    }

    def __init__(self, **kwargs):
        self.offset: int = None
        self.stride: int = None
        self.length: int = None

        get_values_from_kwargs(self, TemporalGrid.ATTR_DICT, kwargs)
