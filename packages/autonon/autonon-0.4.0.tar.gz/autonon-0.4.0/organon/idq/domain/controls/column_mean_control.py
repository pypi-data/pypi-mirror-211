""" This module includes ColumnMeanControl"""
from typing import List

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.algorithms.objects.mean_ci_comparison_input import MeanConfidenceIntervalComparisonInput
from organon.idq.domain.algorithms.objects.time_series_comparison_input import TimeSeriesComparisonInput
from organon.idq.domain.algorithms.objects.traffic_light_comparison_input import TrafficLightComparisonInput
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.controls.helpers.traffic_light_comparer import TrafficLightComparer
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType
from organon.idq.domain.settings.abstractions.dq_base_comparison_parameters import DqBaseComparisonParameters


class ColumnMeanControl(BaseDqControl):
    """ ColumnMeanControl class"""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        """ :returns test group type of control"""
        return DqTestGroupType.MODELLING_AND_CI_CONTROLS_COLUMN_SET

    @staticmethod
    def get_control_type() -> DqControlType:
        """ :returns control type of control"""
        return DqControlType.COLUMN_MEAN

    def _execute_control(self) -> List[DqComparisonResult]:
        """ :returns list of comparison results"""
        results = []
        if self.comp_context.control_results is None:
            raise ValueError("Control results None")
        if self.comp_context.test_calc_result is None:
            raise ValueError("Test result None")
        numerical_comp_cols = self.comp_context.get_comparison_cols_by_native_type(ColumnNativeType.Numeric)
        test_group_info = self.comp_context.test_group_info[self.get_test_group_type()]
        for col in numerical_comp_cols:
            col_name = col.column_name
            effective_bmh = min(test_group_info.test_bmh, col.benchmark_horizon)
            max_index = max(len(self.comp_context.control_results) - effective_bmh, 0)
            filtered_controls = list(self.comp_context.control_results[max_index:])
            test_stat_collection = self.comp_context.test_calc_result.sample_stats.numerical_statistics
            if len(filtered_controls) > 0 and col_name in test_stat_collection:
                control_trimmed_means = [control.sample_stats.numerical_statistics[col_name].trimmed_mean for control in
                                         filtered_controls if col_name in control.sample_stats.numerical_statistics]
                if len(control_trimmed_means) == 0:
                    LogHelper.info(f"Numeric Controls skipped, no past value for {col_name} found")
                else:
                    test_numerical_stats = test_stat_collection[col_name]
                    test_mean = test_numerical_stats.trimmed_mean
                    mi_input = self.__get_mi_input(col_name, control_trimmed_means,
                                                   self.comp_context.comparison_parameters, test_mean)
                    tl_input = self.__get_tl_input(col_name, control_trimmed_means,
                                                   self.comp_context.comparison_parameters, test_mean)
                    ts_input = self.__get_ts_input(col_name, control_trimmed_means,
                                                   self.comp_context.comparison_parameters, test_mean, effective_bmh)
                    results.extend(TrafficLightComparer.get_mi_tl_comparison_results(mi_input, tl_input))
                    results.extend(TrafficLightComparer.get_dq_comparison_results_for_time_series(ts_input))
        return results

    def get_description(self) -> str:
        """ :returns description of control"""
        return "Column Mean Controls"

    @staticmethod
    def __get_mi_input(col: str, past_series: List[float],
                       comp_parameters: DqBaseComparisonParameters,
                       current_val: float) -> MeanConfidenceIntervalComparisonInput:
        """:returns mean confidence interval comparison input"""
        mi_input = MeanConfidenceIntervalComparisonInput()
        mi_input.data_entity = DataEntityType.COLUMN
        mi_input.data_entity_name = col
        mi_input.test_group = ColumnMeanControl.get_test_group_type()
        mi_input.past_series = past_series
        mi_input.current_value = current_val
        mi_input.z_score = comp_parameters.z_score
        mi_input.result_code = DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_MEAN_CONFIDENCE_INTERVAL
        mi_input.message = f"Column {col} mean is outside mean confidence interval."
        return mi_input

    @staticmethod
    def __get_tl_input(col: str, past_series: List[float],
                       comp_parameters: DqBaseComparisonParameters, current_val: float) -> TrafficLightComparisonInput:
        """ :returns traffic light comparer comparison input"""
        tl_input = TrafficLightComparisonInput()
        tl_input.data_entity = DataEntityType.COLUMN
        tl_input.data_entity_name = col
        tl_input.test_group = ColumnMeanControl.get_test_group_type()
        tl_input.past_series = past_series
        tl_input.current_value = current_val
        tl_input.green_threshold = comp_parameters.traffic_light_threshold_green
        tl_input.yellow_threshold = comp_parameters.traffic_light_threshold_yellow
        tl_input.result_code = DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_MEAN_TRAFFIC_LIGHT_INTERVAL
        tl_input.message = f"Column {col} mean is outside mean traffic light interval."
        return tl_input

    @staticmethod
    def __get_ts_input(col: str, past_series: List[float], comp_parameters: DqBaseComparisonParameters,
                       current_val: float, bmh: int) -> TimeSeriesComparisonInput:
        """ :returns time series comparison input"""
        ts_input = TimeSeriesComparisonInput()
        ts_input.data_entity = DataEntityType.COLUMN
        ts_input.data_entity_name = col
        ts_input.test_group = ColumnMeanControl.get_test_group_type()
        ts_input.past_series = past_series
        ts_input.current_value = current_val
        ts_input.bmh = bmh
        ts_input.z_score = comp_parameters.z_score
        ts_input.green_threshold = comp_parameters.traffic_light_threshold_green
        ts_input.yellow_threshold = comp_parameters.traffic_light_threshold_yellow
        ts_input.ad_code = DqComparisonResultCode.COLUMN_MEAN_ABSOLUTE_DEVIATION_FROM_PREDICTION_IS_MAXIMUM
        ts_input.ci_code = DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_PREDICTION_CONFIDENCE_INTERVAL
        ts_input.tl_code = DqComparisonResultCode.COLUMN_MEAN_IS_OUTSIDE_PREDICTION_TRAFFIC_LIGHT_INTERVAL
        ts_input.ad_message = f"Column {col} absolute deviation from prediction is maximum."
        ts_input.ci_message = f"Column {col} is outside prediction confidence interval."
        ts_input.tl_message = f"Column {col} is outside prediction traffic light interval."
        return ts_input
