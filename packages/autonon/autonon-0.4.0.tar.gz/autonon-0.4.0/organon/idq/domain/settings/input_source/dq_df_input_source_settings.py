"""Includes DqDfInputSourceSettings class."""

from organon.idq.domain.businessobjects.record_sources.dq_df_record_source import DqDfRecordSource
from organon.idq.domain.settings.abstractions.dq_base_input_source_settings import DqBaseInputSourceSettings


class DqDfInputSourceSettings(DqBaseInputSourceSettings[DqDfRecordSource]):
    """DQ input source settings for dataframe source type"""

    def __init__(self, source: DqDfRecordSource):
        super().__init__(source)
