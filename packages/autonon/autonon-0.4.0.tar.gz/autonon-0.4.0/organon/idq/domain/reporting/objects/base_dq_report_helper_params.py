"""Includes BaseDqReportHelperParams class."""
import abc
from typing import List

from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.enums.dq_run_type import DqRunType
from organon.idq.domain.settings.partition_info import PartitionInfo


class BaseDqReportHelperParams(metaclass=abc.ABCMeta):
    """Params for DQ report helper."""

    def __init__(self, data_source_name: str, comparison_results: List[DqComparisonResult],
                 data_column_collection: DqDataColumnCollection, run_type: DqRunType,
                 partition: List[PartitionInfo] = None):
        self.data_source_name = data_source_name
        self.partition: List[PartitionInfo] = partition
        self.comparison_results = comparison_results
        self.data_column_collection = data_column_collection
        self.run_type = run_type
        self.filter_str: str = None
