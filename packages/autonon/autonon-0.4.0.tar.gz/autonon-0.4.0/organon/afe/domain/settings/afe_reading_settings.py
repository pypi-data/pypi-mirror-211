"""
This module includes AfeReadngSettings class.
"""
from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class AfeDataReadingSettings:
    """Contains settings for record source reading process"""
    ATTR_DICT = {
        "number_of_rows_per_step": int
    }

    def __init__(self, **kwargs):
        self.number_of_rows_per_step: int = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
