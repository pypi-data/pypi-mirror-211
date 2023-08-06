"""Includes SourceWithPartitionsReportHelperParams class."""
from typing import List

from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.enums.dq_run_type import DqRunType
from organon.idq.domain.reporting.objects.base_multiple_calculation_report_helper_params import \
    BaseMultipleCalculationReportHelperParams
from organon.idq.domain.settings.partition_info import PartitionInfo


class SourceWithPartitionsReportHelperParams(BaseMultipleCalculationReportHelperParams):
    """Params for DQ report helper."""

    def __init__(self, data_source_name: str, comparison_results: List[DqComparisonResult],
                 data_column_collection: DqDataColumnCollection, run_type: DqRunType,
                 partition: List[PartitionInfo] = None):
        super().__init__(data_source_name, comparison_results, data_column_collection, run_type,
                         partition=partition)
