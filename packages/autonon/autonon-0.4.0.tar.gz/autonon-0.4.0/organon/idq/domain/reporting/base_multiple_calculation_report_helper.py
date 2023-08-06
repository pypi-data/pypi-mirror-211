"""Includes BaseMultipleSourceReportHelper class."""
import abc
from typing import List, TypeVar, Generic

import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.reporting.base_dq_report_helper import BaseDqReportHelper
from organon.idq.domain.reporting.objects.base_alert_info import BaseAlertInfo
from organon.idq.domain.reporting.objects.base_dq_output_report import BaseDqOutputReport
from organon.idq.domain.reporting.objects.base_multiple_calculation_report_helper_params import \
    BaseMultipleCalculationReportHelperParams
from organon.idq.domain.reporting.objects.dq_comparison_sample_report_input import DqComparisonSampleReportInput
from organon.idq.domain.reporting.objects.nominal_column_control_details import NominalColumnControlDetails
from organon.idq.domain.reporting.objects.numeric_column_control_details import NumericColumnControlDetails
from organon.idq.domain.reporting.objects.table_control_details import TableControlDetails

DqComparisonSampleReportInputType = TypeVar("DqComparisonSampleReportInputType", bound=DqComparisonSampleReportInput)


class BaseMultipleCalculationReportHelper(Generic[DqComparisonSampleReportInputType], BaseDqReportHelper):
    """Includes helper methods for BaseMultipleSourceReportHelper"""

    def __init__(self, base_multiple_source_dq_report_helper_params: BaseMultipleCalculationReportHelperParams):
        super().__init__(base_multiple_source_dq_report_helper_params)
        self.calculation_count = base_multiple_source_dq_report_helper_params.calculation_count
        self.comparison_column_info = base_multiple_source_dq_report_helper_params.comparison_column_info
        self.sample_statistics = base_multiple_source_dq_report_helper_params.sample_statistics
        self.population_statistics = base_multiple_source_dq_report_helper_params.population_statistics
        self.data_source_statistics = base_multiple_source_dq_report_helper_params.data_source_statistics

    @abc.abstractmethod
    def execute(self) -> BaseDqOutputReport:
        """Execute reporting for one df"""
        raise NotImplementedError

    @abc.abstractmethod
    def _get_table_alert(self, table_comparison_result):
        """Return alert of table"""
        raise NotImplementedError

    @staticmethod
    def _get_numeric_alert_list(calculation_count: int) -> List[DqComparisonResultCode]:
        if calculation_count >= 5:
            numeric_alert_list = [DqComparisonResultCode.COLUMN_MEAN_ABSOLUTE_DEVIATION_FROM_PREDICTION_IS_MAXIMUM,
                                  DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_MEAN_CONFIDENCE_INTERVAL,
                                  DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_MEAN_TRAFFIC_LIGHT_INTERVAL,
                                  DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_PREDICTION_CONFIDENCE_INTERVAL,
                                  DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_PREDICTION_TRAFFIC_LIGHT_INTERVAL,
                                  DqComparisonResultCode.PSI_RED_SIGNAL
                                  ]
        else:
            numeric_alert_list = [DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_MEAN_TRAFFIC_LIGHT_INTERVAL,
                                  DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_MEAN_CONFIDENCE_INTERVAL,
                                  DqComparisonResultCode.PSI_RED_SIGNAL
                                  ]
        return numeric_alert_list

    @staticmethod
    def _get_column_stability_alert_list() -> List[DqComparisonResultCode]:
        alert_list = [DqComparisonResultCode.COLUMN_IS_CONSTANT,
                      DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_ZERO,
                      DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_NULL]
        return alert_list

    @staticmethod
    def _get_table_alert_list(calculation_count: int) -> List[DqComparisonResultCode]:
        if calculation_count >= 5:
            table_alert_list = [DqComparisonResultCode.ROW_COUNT_ABSOLUTE_DEVIATION_FROM_PREDICTION_IS_MAXIMUM,
                                DqComparisonResultCode.ROW_COUNT_IS_OUTSIDE_PREDICTION_CONFIDENCE_INTERVAL,
                                DqComparisonResultCode.ROW_COUNT_IS_OUTSIDE_PREDICTION_TRAFFIC_LIGHT_INTERVAL,
                                DqComparisonResultCode.ROW_COUNT_MEAN_IS_OUTSIDE_MEAN_CONFIDENCE_INTERVAL,
                                DqComparisonResultCode.ROW_COUNT_MEAN_IS_OUTSIDE_MEAN_TRAFFIC_LIGHT_INTERVAL
                                ]
        else:
            table_alert_list = [DqComparisonResultCode.ROW_COUNT_MEAN_IS_OUTSIDE_MEAN_CONFIDENCE_INTERVAL,
                                DqComparisonResultCode.ROW_COUNT_MEAN_IS_OUTSIDE_MEAN_TRAFFIC_LIGHT_INTERVAL]
        return table_alert_list

    @abc.abstractmethod
    def _get_numeric_column_alert(self, numeric_comparison_result):
        """Return numeric column alert of table"""
        raise NotImplementedError

    @abc.abstractmethod
    def _get_nominal_column_alert(self, nominal_comparison_result):
        """Return nominal column alert of table"""
        raise NotImplementedError

    def _get_alert_data(self) -> List[BaseAlertInfo]:
        """Return alert data multiple data sources"""
        list_base_alert_info: List[BaseAlertInfo] = []
        table_comparison_result, numeric_comparison_result, nominal_comparison_result = self._get_result_with_type()
        table_comparison_result_list = [result.result_code for result in table_comparison_result]
        table_alert = self._get_table_alert(table_comparison_result_list)
        list_base_alert_info.extend(table_alert)
        numeric_column_alert = self._get_numeric_column_alert(numeric_comparison_result)
        list_base_alert_info.extend(numeric_column_alert)
        nominal_column_alert = self._get_nominal_column_alert(nominal_comparison_result)
        list_base_alert_info.extend(nominal_column_alert)
        return list_base_alert_info

    def _get_report_data(self) -> DqComparisonSampleReportInputType:

        report_data = self._get_report_input_instance()
        report_data.dq_data_column_collection = self.data_column_collection
        report_data.dq_comparison_result = self.comparison_results
        alert_info_list = self._get_alert_data()
        report_data.alert_info = alert_info_list
        report_data.numeric_columns_control = self._get_numeric_column_details(alert_info_list)
        report_data.nominal_columns_control = self._get_nominal_column_details(alert_info_list)
        report_data.table_control = self._get_table_control_details(alert_info_list)

        return report_data

    @classmethod
    def _get_report_input_instance(cls) -> DqComparisonSampleReportInputType:
        return DqComparisonSampleReportInput()

    def _get_numeric_column_details(self, alert_info: List[BaseAlertInfo]) \
            -> List[NumericColumnControlDetails]:
        """Return numeric column details"""
        list_numeric_column_details: List[NumericColumnControlDetails] = []
        alert_column_list = {alert.alert for alert in alert_info}
        for state_of_benchmark, (calculation_name, sample_stats) in enumerate(self.sample_statistics.items()):
            numeric_stats_dict = sample_stats.numerical_statistics
            for column_name, numeric_stats in numeric_stats_dict.items():
                if column_name in alert_column_list:
                    numeric_column_details = NumericColumnControlDetails()
                    numeric_column_details.calculation_name = calculation_name
                    numeric_column_details.column_name = column_name
                    numeric_column_details.column_type = ColumnNativeType.Numeric
                    numeric_column_details.mean = numeric_stats.mean
                    numeric_column_details.trimmed_mean = numeric_stats.trimmed_mean
                    numeric_column_details.state_of_benchmark = state_of_benchmark + 1
                    list_numeric_column_details.append(numeric_column_details)
        return list_numeric_column_details

    def _get_nominal_column_details(self, alert_info: List[BaseAlertInfo]) \
            -> List[NominalColumnControlDetails]:
        """Return nominal column details"""
        list_nominal_column_details: List[NominalColumnControlDetails] = []
        alert_column_list = {alert.alert for alert in alert_info}

        for state_of_benchmark, (calculation_name, population_stats) in enumerate(self.population_statistics.items()):
            population_statistics = population_stats.nominal_statistics
            for column_name, nominal_stats in population_statistics.items():
                if column_name in alert_column_list:
                    data_column = self.data_column_collection.get_column(column_name)
                    value = self._get_nominal_value_for_column(column_name)
                    nominal_column_details = NominalColumnControlDetails()
                    nominal_column_details.calculation_name = calculation_name
                    nominal_column_details.column_name = column_name
                    nominal_column_details.column_type = data_column.column_native_type
                    if value in nominal_stats.percentages:
                        nominal_column_details.percentage = nominal_stats.percentages[value]
                    else:
                        nominal_column_details.percentage = 0
                    nominal_column_details.state_of_benchmark = state_of_benchmark + 1
                    nominal_column_details.value = value
                    list_nominal_column_details.append(nominal_column_details)
        return list_nominal_column_details

    def _get_table_control_details(self, alert_info: List[BaseAlertInfo]) -> List[TableControlDetails]:
        """Return table control details"""
        list_table_control_details: List[TableControlDetails] = []
        alert_column_list = {alert.alert for alert in alert_info}
        if DataEntityType.TABLE.name in alert_column_list:
            for state_of_benchmark, (calculation_name, table_stats) in enumerate(self.data_source_statistics.items()):
                table_size = table_stats.size_in_bytes
                row_count = table_stats.row_count
                if table_size is not None:
                    if table_size > 0:
                        table_control_details = TableControlDetails()
                        table_control_details.calculation_name = calculation_name
                        table_control_details.type = DataEntityType.TABLE
                        table_control_details.property_key = "TableSizeInBytes"
                        table_control_details.value = table_size
                        table_control_details.state_of_benchmark = state_of_benchmark + 1
                        list_table_control_details.append(table_control_details)
                if row_count is not None:
                    if row_count > 0:
                        table_control_details = TableControlDetails()
                        table_control_details.calculation_name = calculation_name
                        table_control_details.type = DataEntityType.TABLE
                        table_control_details.property_key = "RowCount"
                        table_control_details.value = row_count
                        table_control_details.state_of_benchmark = state_of_benchmark + 1
                        list_table_control_details.append(table_control_details)
        return list_table_control_details

    def _get_nominal_value_for_column(self, column_name: str) -> List[str]:
        """Return value  of nominal columns"""
        value = None
        for comp in self.comparison_results:
            if comp.data_entity_name == column_name and comp.property_code == "MaximumPsiCategory":
                value = comp.property_key_nominal
        return value

    @staticmethod
    def _get_alert_df(report_data: DqComparisonSampleReportInputType):
        alert_list = report_data.alert_info
        alerts_df = pd.DataFrame.from_records([a.to_dict() for a in alert_list])
        alerts_df = alerts_df.drop_duplicates(
            subset=alerts_df.columns,
            keep='last').reset_index(drop=True)
        return alerts_df

    @staticmethod
    def _get_signal_df(report_data: DqComparisonSampleReportInputType):
        signal_list = BaseMultipleCalculationReportHelper._get_signal_details(report_data)
        signals_df = pd.DataFrame.from_records([s.to_dict() for s in signal_list])
        signals_df = signals_df.drop_duplicates(
            subset=signals_df.columns,
            keep='last').reset_index(drop=True)
        return signals_df

    @staticmethod
    def _get_numeric_columns_control_df(report_data: DqComparisonSampleReportInputType):
        numeric_columns_control_list = report_data.numeric_columns_control
        numeric_columns_control_df = pd.DataFrame.from_records([num.to_dict() for num in numeric_columns_control_list])
        return numeric_columns_control_df

    @staticmethod
    def _get_nominal_columns_control_df(report_data: DqComparisonSampleReportInputType):
        nominal_columns_control_list = report_data.nominal_columns_control
        nominal_columns_control_df = pd.DataFrame.from_records([nom.to_dict() for nom in nominal_columns_control_list])
        return nominal_columns_control_df

    @staticmethod
    def _get_table_control_df(report_data: DqComparisonSampleReportInputType):
        table_control_list = report_data.table_control
        table_control_df = pd.DataFrame.from_records([t.to_dict() for t in table_control_list])
        return table_control_df

    def _fill_output_report(self, report_data: DqComparisonSampleReportInputType, output_report):
        output_report.alerts_df = self._get_alert_df(report_data)
        output_report.signals_df = self._get_signal_df(report_data)
        output_report.signals = report_data.dq_comparison_result
        output_report.column_collection = report_data.dq_data_column_collection
        output_report.numeric_column_control_details_df = self._get_numeric_columns_control_df(report_data)
        output_report.nominal_column_control_details_df = self._get_nominal_columns_control_df(report_data)
        output_report.table_control_details_df = self._get_table_control_df(report_data)
        return output_report
