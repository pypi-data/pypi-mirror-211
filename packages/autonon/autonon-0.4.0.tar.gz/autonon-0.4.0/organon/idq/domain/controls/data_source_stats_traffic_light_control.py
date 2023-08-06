"""Includes DataSourceStatsTrafficLightControl class."""
from typing import List

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.algorithms.objects.mean_ci_comparison_input import MeanConfidenceIntervalComparisonInput
from organon.idq.domain.algorithms.objects.traffic_light_comparison_input import TrafficLightComparisonInput
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.controls.helpers.traffic_light_comparer import TrafficLightComparer
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class DataSourceStatsTrafficLightControl(BaseDqControl):
    """Control for data source statistics using Traffic Light """

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.TRAFFIC_LIGHT_CONTROLS

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.DATA_SOURCE_STATS_TL_CONTROL

    def get_description(self) -> str:
        return "Row Count Traffic Light Control"

    def _execute_control(self) -> List[DqComparisonResult]:
        bmh = self.get_test_bmh()
        if bmh < 1:
            raise ValueError("Bmh should be greater than or equal to 1")
        row_count_series = self.__get_row_count_series()
        row_count_current_value = self.comp_context.test_calc_result.data_source_stats.row_count

        results = TrafficLightComparer.get_mi_tl_comparison_results(
            self.__get_ci_comparison_input(row_count_series, row_count_current_value),
            self.__get_tl_comparison_input(row_count_series, row_count_current_value)
        )
        return results

    def __get_tl_comparison_input(self, series: List[float],
                                  current_value: int) -> TrafficLightComparisonInput:
        inp = TrafficLightComparisonInput()
        inp.test_group = self.get_test_group_type()
        inp.data_entity = DataEntityType.TABLE
        inp.data_entity_name = self.comp_context.test_calc_parameters.input_source_settings.source.get_name()
        inp.past_series = series
        inp.current_value = current_value
        inp.green_threshold = self.comp_context.comparison_parameters.traffic_light_threshold_green
        inp.yellow_threshold = self.comp_context.comparison_parameters.traffic_light_threshold_yellow
        inp.result_code = DqComparisonResultCode.ROW_COUNT_MEAN_IS_OUTSIDE_MEAN_TRAFFIC_LIGHT_INTERVAL
        inp.message = "Mean value for the historical row-count is statistically different from current row-count"
        return inp

    def __get_ci_comparison_input(self, series: List[float], current_value: int) \
            -> MeanConfidenceIntervalComparisonInput:
        inp = MeanConfidenceIntervalComparisonInput()
        inp.test_group = self.get_test_group_type()
        inp.data_entity = DataEntityType.TABLE
        inp.data_entity_name = self.comp_context.test_calc_parameters.input_source_settings.source.get_name()
        inp.past_series = series
        inp.current_value = current_value
        inp.z_score = self.comp_context.comparison_parameters.z_score
        inp.result_code = DqComparisonResultCode.ROW_COUNT_MEAN_IS_OUTSIDE_MEAN_CONFIDENCE_INTERVAL
        inp.message = "Mean value for the historical row-count series is statistically different from current row-count"
        return inp

    def __get_row_count_series(self) -> List[float]:
        series = []
        bmh = self.get_test_bmh()
        control_results = self.comp_context.control_results
        row_count_eligible = 0
        for i in range(len(control_results) - 1, -1, -1):
            row_count = control_results[i].data_source_stats.row_count
            if row_count is not None and row_count_eligible < bmh:
                series.append(float(row_count))
                row_count_eligible += 1
        return list(reversed(series))
