"""
This module includes AfeSettingsReader class.
"""
from organon.afe.domain.common.reader_helper import setattr_if_none
from organon.afe.domain.settings.afe_modelling_settings import AfeModellingSettings
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.base_afe_settings_reader import BaseAfeSettingsReader


class AfeSettingsReader(BaseAfeSettingsReader[AfeModellingSettings]):
    """
    Class for static methods on reading AfeModellingSettings from a file
    """

    def _set_trx_descriptor_defaults(self, modelling_settings: AfeModellingSettings):

        feature_gen_settings = modelling_settings.data_source_settings.trx_descriptor.feature_gen_setting

        if feature_gen_settings.included_operators is None:
            feature_gen_settings.included_operators = self._get_default_included_afe_operators()
        if feature_gen_settings.date_offset is None:
            feature_gen_settings.date_offset = 0
        try:
            trx_descriptor = modelling_settings.data_source_settings.trx_descriptor
            if trx_descriptor.reading_settings is None:
                trx_descriptor.reading_settings = AfeDataReadingSettings()

            setattr_if_none(trx_descriptor.reading_settings, "number_of_rows_per_step", 100000)

        except AttributeError:
            pass
