"""Includes DqFileRecordSource class."""
from organon.idq.domain.businessobjects.record_sources.dq_base_record_source import DqBaseRecordSource
from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType


class DqFileRecordSource(DqBaseRecordSource[str]):
    """Dq record source for text file objects."""

    def __init__(self, locator: str):
        super().__init__(locator)

    def get_name(self) -> str:
        return f"File({self.locator})"

    @staticmethod
    def get_type() -> DqRecordSourceType:
        return DqRecordSourceType.TEXT
