"""Includes DqFileInputSourceSettings class."""
from typing import List

from organon.idq.domain.businessobjects.record_sources.dq_file_record_source import DqFileRecordSource
from organon.idq.domain.settings.abstractions.dq_base_input_source_settings import DqBaseInputSourceSettings


class DqFileInputSourceSettings(DqBaseInputSourceSettings[DqFileRecordSource]):
    """DQ input source settings for file source type"""

    def __init__(self, source: DqFileRecordSource):
        super().__init__(source)
        self.number_of_rows_per_step: int = None
        self.csv_separator: str = None
        self.date_columns: List[str] = None
