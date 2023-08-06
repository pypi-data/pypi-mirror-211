"""Includes DqDfRecordSource class."""
import pandas as pd

from organon.idq.domain.businessobjects.record_sources.dq_base_record_source import DqBaseRecordSource
from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType


class DqDfRecordSource(DqBaseRecordSource[pd.DataFrame]):
    """Dq record source for pandas dataframe objects."""

    def __init__(self, locator: pd.DataFrame, name: str):
        super().__init__(locator)
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    @staticmethod
    def get_type() -> DqRecordSourceType:
        return DqRecordSourceType.DATA_FRAME
