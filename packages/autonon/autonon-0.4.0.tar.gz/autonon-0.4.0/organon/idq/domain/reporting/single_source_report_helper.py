"""Includes SingleSourceReportHelper class."""
from typing import List

import pandas as pd

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.domain.reporting.base_dq_report_helper import BaseDqReportHelper
from organon.idq.domain.reporting.objects.dq_comparison_sample_report_input import DqComparisonSampleReportInput
from organon.idq.domain.reporting.objects.single_source_alert_info import SingleSourceAlertInfo
from organon.idq.domain.reporting.objects.single_source_report_helper_params import SingleSourceReportHelperParams
from organon.idq.domain.reporting.objects.single_source_report_output import SingleSourceOutputReport


class SingleSourceReportHelper(BaseDqReportHelper):
    """Includes helper methods for one df reporting DQ execution results"""

    def __init__(self, params: SingleSourceReportHelperParams):
        super().__init__(params)
        self.params: SingleSourceReportHelperParams = params

    def execute(self) -> SingleSourceOutputReport:
        """Execute reporting for one df"""
        report_data = self._get_report_data()
        alert_list = report_data.alert_info
        alerts_df = pd.DataFrame.from_records([a.to_dict() for a in alert_list])
        alerts_df_unique = alerts_df.drop_duplicates(
            subset=alerts_df.columns,
            keep='last').reset_index(drop=True)
        signal_list = SingleSourceReportHelper._get_signal_details(report_data)
        signals_df = pd.DataFrame.from_records([s.to_dict() for s in signal_list])
        output_report = SingleSourceOutputReport()
        output_report.alerts_df = alerts_df_unique
        output_report.signals_df = signals_df
        output_report.signals = report_data.dq_comparison_result
        output_report.column_collection = report_data.dq_data_column_collection
        return output_report

    def _get_report_data(self) -> DqComparisonSampleReportInput:

        report_data = DqComparisonSampleReportInput()
        report_data.dq_data_column_collection = self.data_column_collection
        report_data.dq_comparison_result = self.comparison_results
        alert_info_list = self._get_alert_data()
        report_data.alert_info = alert_info_list
        return report_data

    def _get_alert_data(self) -> List[SingleSourceAlertInfo]:

        list_base_alert_info: List[SingleSourceAlertInfo] = []
        for comparison_result in self.comparison_results:
            alert_info = SingleSourceAlertInfo()
            alert_info.data_source_name = self.data_source_name
            if comparison_result.data_entity == DataEntityType.TABLE:
                alert = DataEntityType.TABLE.name
            else:
                alert = comparison_result.data_entity_name
            alert_info.alert = alert
            alert_info.full_filter_str = self._get_full_filter_string(self.params.partition, self.params.filter_str)
            alert_info.run_type = self.run_type
            list_base_alert_info.append(alert_info)

        return list_base_alert_info
