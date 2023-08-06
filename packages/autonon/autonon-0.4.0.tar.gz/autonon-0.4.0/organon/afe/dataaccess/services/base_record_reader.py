"""
This module includes RecordReader class.
"""
import abc

from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.fl.core.exceptionhandling.known_exception import KnownException


class BaseRecordReader(metaclass=abc.ABCMeta):
    """Base class for record reader classes."""

    def __init__(self, record_source: RecordSource):
        self._record_source: RecordSource = record_source

    def read(self):
        """
        Reads the table of records and returns a collection
        :return: A collection containing records in record source
        """
        source_type = self._record_source.get_type()
        if source_type == RecordSourceType.DATABASE:
            return self.read_db_source()
        if source_type == RecordSourceType.TEXT:
            return self.read_text_source()
        if source_type == RecordSourceType.DATA_FRAME:
            return self.read_dataframe_source()
        raise KnownException("Record source type is not valid!")

    @abc.abstractmethod
    def read_text_source(self):
        """Reads text source and returns a collection"""

    @abc.abstractmethod
    def read_dataframe_source(self):
        """Reads DataFrame source and returns a collection"""

    @abc.abstractmethod
    def read_db_source(self):
        "Reads database source and returns a collection"
