"""
This module includes TransactionFileDescriptor class.
"""
import abc

from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.record_source import RecordSource


class BaseTrxDescriptor(metaclass=abc.ABCMeta):
    """
    Class for information about transaction file or database table
    """
    ATTR_DICT = {
        "modelling_raw_input_source": RecordSource,
        "entity_column_name": str,
        "reading_settings": AfeDataReadingSettings
    }

    def __init__(self, **kwargs):
        self.modelling_raw_input_source: RecordSource = None
        self.entity_column_name: str = None
        self.reading_settings: AfeDataReadingSettings = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)

    @abc.abstractmethod
    def get_all_dimension_and_quantity_columns(self):
        """Returns sets of all dimension and quantity columns defined in date column settings"""
