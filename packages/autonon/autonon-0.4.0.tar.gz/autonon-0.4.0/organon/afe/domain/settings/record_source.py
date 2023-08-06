"""
This module includes TargetRecordSource class.
"""
from typing import Union

import pandas as pd

from organon.afe.domain.settings.db_object_input import DbObjectInput
from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.fl.core.exceptionhandling.known_exception import KnownException


class RecordSource:
    """
    Description of a target record source.
    """

    def __init__(self, **kwargs):
        self.source: Union[DbObjectInput, pd.DataFrame, str] = None

        if "source" in kwargs:
            source = kwargs["source"]
            if isinstance(source, dict):
                self.source = DbObjectInput(**source)
            elif isinstance(source, (str, DbObjectInput, pd.DataFrame)):
                self.source = source
            else:
                raise KnownException("source should be dict, file path string, DbObjectInput or pd.DataFrame")

    def get_type(self) -> RecordSourceType:
        """Returns type of the source"""
        if isinstance(self.source, DbObjectInput):
            return RecordSourceType.DATABASE
        if isinstance(self.source, pd.DataFrame):
            return RecordSourceType.DATA_FRAME
        if isinstance(self.source, str):
            return RecordSourceType.TEXT
        raise KnownException("Record source type is not valid!")
