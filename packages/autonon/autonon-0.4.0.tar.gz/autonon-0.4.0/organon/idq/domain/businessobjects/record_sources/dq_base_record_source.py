"""
This module includes TargetRecordSource class.
"""
import abc
from typing import TypeVar, Generic

from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType

DqSourceLocatorType = TypeVar("DqSourceLocatorType")


class DqBaseRecordSource(Generic[DqSourceLocatorType], metaclass=abc.ABCMeta):
    """
    Description of a dq record source.
    """

    def __init__(self, locator: DqSourceLocatorType):
        self.locator: DqSourceLocatorType = locator

    @abc.abstractmethod
    def get_name(self) -> str:
        """Returns name of the record source"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_type() -> DqRecordSourceType:
        """Returns type of the source"""
        raise NotImplementedError
