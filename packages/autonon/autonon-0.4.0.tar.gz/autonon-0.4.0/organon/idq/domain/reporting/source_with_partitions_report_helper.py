"""Includes SourceWithDateReportHelper class."""
from typing import List

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.reporting.base_multiple_calculation_report_helper import BaseMultipleCalculationReportHelper
from organon.idq.domain.reporting.objects.source_with_partitions_alert_info import SourceWithPartitionsAlertInfo
from organon.idq.domain.reporting.objects.source_with_partitions_dq_report_output import \
    SourceWithPartitionsDqOutputReport
from organon.idq.domain.reporting.objects.source_with_partitions_report_helper_params import \
    SourceWithPartitionsReportHelperParams


class SourceWithPartitionsReportHelper(BaseMultipleCalculationReportHelper):
    """Includes helper methods for one df with date reporting DQ execution results"""

    def __init__(self, params: SourceWithPartitionsReportHelperParams):
        super().__init__(params)
        self.params = params

    def execute(self) -> SourceWithPartitionsDqOutputReport:
        """Execute reporting for one df"""

        report_data = self._get_report_data()
        output_report = SourceWithPartitionsDqOutputReport()
        self._fill_output_report(report_data, output_report)
        return output_report

    def _get_table_alert(self, table_comparison_result):
        table_alert_list = self._get_table_alert_list(self.calculation_count)
        alert_list = []

        if all(elem in table_comparison_result for elem in table_alert_list):
            alert_info = SourceWithPartitionsAlertInfo()
            alert_info.data_source_name = self.data_source_name
            alert_info.alert = DataEntityType.TABLE.name
            alert_info.run_type = self.run_type
            alert_info.full_filter_str = self._get_full_filter_string(self.params.partition,
                                                                      self.params.filter_str)
            alert_list.append(alert_info)
        return alert_list

    def _get_numeric_column_alert(self, numeric_comparison_result):
        numeric_alert_list = self._get_numeric_alert_list(self.calculation_count)
        column_stability_alert_list = self._get_column_stability_alert_list()

        return self._get_alert_list(numeric_comparison_result, numeric_alert_list, column_stability_alert_list)

    def _get_nominal_column_alert(self, nominal_comparison_result):
        nominal_alert_list = [DqComparisonResultCode.PSI_RED_SIGNAL]
        column_stability_alert_list = self._get_column_stability_alert_list()

        return self._get_alert_list(nominal_comparison_result, nominal_alert_list, column_stability_alert_list)

    def _get_alert_list(self, results: List[DqComparisonResult], alert_codes: List[DqComparisonResultCode],
                        column_stability_alert_list: List[DqComparisonResultCode]):
        column_results = self._get_result_dict(results)
        alert_list = []
        for column_name, result_code in column_results.items():
            if all(elem in result_code for elem in alert_codes) or \
                    any(elem in result_code for elem in column_stability_alert_list):
                alert_info = SourceWithPartitionsAlertInfo()
                alert_info.data_source_name = self.data_source_name
                alert_info.alert = column_name
                alert_info.run_type = self.run_type
                alert_info.full_filter_str = self._get_full_filter_string(self.params.partition, self.params.filter_str)
                alert_list.append(alert_info)
        return alert_list
