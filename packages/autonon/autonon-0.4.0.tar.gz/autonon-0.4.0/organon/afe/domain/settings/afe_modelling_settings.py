"""
This module includes AfeModellingSettings class.
"""

from organon.afe.domain.settings.afe_data_settings import AfeDataSettings
from organon.afe.domain.settings.afe_output_settings import AfeOutputSettings
from organon.afe.domain.settings.base_afe_modelling_settings import BaseAfeModellingSettings


class AfeModellingSettings(BaseAfeModellingSettings[AfeDataSettings, AfeOutputSettings]):
    """
    Modelling Settings for Automated Feature Extraction
    """
    ATTR_DICT = {
        "data_source_settings": AfeDataSettings,
        "output_settings": AfeOutputSettings,
    }
    ATTR_DICT.update(BaseAfeModellingSettings.ATTR_DICT)
