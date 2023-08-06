"""
This module includes AfeDataSettings class.
"""

from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.settings.base_afe_data_settings import BaseAfeDataSettings
from organon.afe.domain.settings.trx_descriptor import TrxDescriptor


class AfeDataSettings(BaseAfeDataSettings[TrxDescriptor]):
    """
    Stores data source settings for AfeModellingSettings
    """
    ATTR_DICT = {
        "trx_descriptor": TrxDescriptor,
    }
    ATTR_DICT.update(BaseAfeDataSettings.ATTR_DICT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
