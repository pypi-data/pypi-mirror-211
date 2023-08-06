"""
This module includes BaseAfeScoringSettings class.
"""
from datetime import datetime
from typing import TypeVar, Generic

from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput
from organon.afe.domain.settings.afe_process_settings import AfeProcessSettings
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.base_afe_settings import BaseAfeSettings
from organon.afe.domain.settings.record_source import RecordSource

AfeModelOutputType = TypeVar("AfeModelOutputType", bound=BaseAfeModelOutput)


class BaseAfeScoringSettings(Generic[AfeModelOutputType], BaseAfeSettings):
    """
    #TODO docstring
    """
    ATTR_DICT = {
        "process_settings": AfeProcessSettings,
        "model_file_path": str,
        "scoring_date": datetime,
        "target_record_source": RecordSource,
        "raw_input_source": RecordSource,
        "trx_reading_settings": AfeDataReadingSettings,
    }

    def __init__(self):
        super().__init__()
        self.model_file_path: str = None
        self.scoring_date: datetime = None
        self.target_record_source: RecordSource = None
        self.raw_input_source: RecordSource = None
        self.model_output: BaseAfeModelOutput = None
        self.trx_reading_settings: AfeDataReadingSettings = None
