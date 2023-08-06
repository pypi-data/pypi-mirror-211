"""Includes BaseDqReportHelper class"""
import abc
from typing import List, Dict

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers import list_helper, string_helper
from organon.idq.core.dq_constants import DqConstants
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.reporting.objects.base_dq_output_report import BaseDqOutputReport
from organon.idq.domain.reporting.objects.base_dq_report_helper_params import BaseDqReportHelperParams
from organon.idq.domain.reporting.objects.dq_comparison_sample_report_input import DqComparisonSampleReportInput
from organon.idq.domain.reporting.objects.signal_details import SignalDetails
from organon.idq.domain.settings.partition_info import PartitionInfo


class BaseDqReportHelper(metaclass=abc.ABCMeta):
    """Class for base dq report  helper"""

    def __init__(self, base_dq_output_helper_params: BaseDqReportHelperParams):
        self.data_source_name = base_dq_output_helper_params.data_source_name
        self.comparison_results = base_dq_output_helper_params.comparison_results
        self.data_column_collection = base_dq_output_helper_params.data_column_collection
        self.run_type = base_dq_output_helper_params.run_type

    @abc.abstractmethod
    def execute(self) -> BaseDqOutputReport:
        """Execute reporting for one df"""
        raise NotImplementedError

    @staticmethod
    def _get_signal_details(dq_comparison_sample_report_input: DqComparisonSampleReportInput) \
            -> List[SignalDetails]:
        """Return alerts"""

        signals: List[SignalDetails] = []
        if dq_comparison_sample_report_input is not None and \
                dq_comparison_sample_report_input.dq_comparison_result is not None:
            for signal in dq_comparison_sample_report_input.dq_comparison_result:
                signal_details = SignalDetails()
                signal_details.data_entity_name = signal.data_entity_name
                if signal.data_entity == DataEntityType.TABLE:
                    signal_details.column_type = DataEntityType.TABLE.name
                else:
                    col = dq_comparison_sample_report_input.dq_data_column_collection.get_column(
                        signal.data_entity_name)
                    if col is not None:
                        signal_details.column_type = col.column_native_type.name
                signal_details.signal = signal.result_code.name
                signals.append(signal_details)
        return signals

    def _get_result_with_type(self):
        """Get result with type : table comparison result, numeric comparison result, nominal comparison result"""
        table_comparison_result = []
        numeric_comparison_result = []
        nominal_comparison_result = []
        for comparison_result in self.comparison_results:
            if comparison_result.data_entity == DataEntityType.TABLE:
                table_comparison_result.append(comparison_result)
            else:
                data_column = self.data_column_collection.get_column(comparison_result.data_entity_name)
                if data_column.column_native_type == ColumnNativeType.Numeric:
                    numeric_comparison_result.append(comparison_result)
                elif data_column.column_native_type in DqConstants.NOMINAL_COLUMN_TYPES:
                    nominal_comparison_result.append(comparison_result)

        return table_comparison_result, numeric_comparison_result, nominal_comparison_result

    def _get_result_dict(self, comparison_result_list: List[DqComparisonResult]) -> \
            Dict[str, List[DqComparisonResultCode]]:
        """Return column- result code result"""
        result: Dict[str, List[DqComparisonResultCode]] = {}
        for comparison_result in comparison_result_list:
            column_name = self.data_column_collection \
                .get_column(comparison_result.data_entity_name).column_name
            if column_name in result:
                result[column_name].append(comparison_result.result_code)
            else:
                result[column_name] = [comparison_result.result_code]
        return result

    @classmethod
    def _get_full_filter_string(cls, partition: List[PartitionInfo], filter_str: str):
        partition_str = cls._get_partition_string(partition)
        if string_helper.is_null_or_empty(partition_str) and string_helper.is_null_or_empty(filter_str):
            return ""
        if not string_helper.is_null_or_empty(partition_str):
            if not string_helper.is_null_or_empty(filter_str):
                return f"Partition:{partition_str} - Filtered By:'{filter_str}'"
            return partition_str
        return f"Filtered By:'{filter_str}'"

    @classmethod
    def _get_partition_string(cls, partition: List[PartitionInfo]) -> str:
        if list_helper.is_null_or_empty(partition):
            return ""
        return " & ".join([partition_info.to_str() for partition_info in partition])
