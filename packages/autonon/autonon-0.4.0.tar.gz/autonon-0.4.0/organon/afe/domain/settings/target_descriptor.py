"""
This module includes TargetFileDescriptor class.
"""
from datetime import datetime

from organon.afe.domain.common.reader_helper import get_values_from_kwargs
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.afe_target_column import AfeTargetColumn


class TargetDescriptor:
    """
    Class for information about target file or database table
    """

    ATTR_DICT = {
        "entity_column_name": str,
        "default_measurement_date": datetime,
        "date_column": AfeDateColumn,
        "target_column": AfeTargetColumn,
        "reading_settings": AfeDataReadingSettings
    }

    def __init__(self, **kwargs):
        self.entity_column_name: str = None
        self.default_measurement_date: datetime = None
        self.date_column: AfeDateColumn = None
        self.target_column: AfeTargetColumn = None
        self.reading_settings: AfeDataReadingSettings = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
