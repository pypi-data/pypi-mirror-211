"""Includes DqBaseInputSourceSettings class."""
import sys
from typing import TypeVar, Generic, List, Callable

import pandas as pd

from organon.idq.domain.businessobjects.record_sources.dq_base_record_source import DqBaseRecordSource
from organon.idq.domain.settings.partition_info import PartitionInfo

DqRecordSourceType = TypeVar("DqRecordSourceType", bound=DqBaseRecordSource)


class DqBaseInputSourceSettings(Generic[DqRecordSourceType]):
    """Base input source settings for input source types"""

    def __init__(self, source: DqRecordSourceType):
        self.source: DqRecordSourceType = source
        self.is_sampling_on: bool = None
        self.sampling_ratio: float = None
        self.max_num_of_samples: int = sys.maxsize
        self.included_columns: List[str] = None
        self.partition_info_list: List[PartitionInfo] = None
        self.filter_callable: Callable[[pd.DataFrame], pd.DataFrame] = None
