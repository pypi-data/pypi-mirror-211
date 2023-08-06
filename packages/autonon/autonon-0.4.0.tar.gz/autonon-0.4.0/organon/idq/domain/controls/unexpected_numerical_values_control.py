"""Includes UnexpectedNumericalValuesControl class."""
import math
from typing import List

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.core.helpers.formatting_helper import FormattingHelper
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.statistics.dq_sample_numerical_statistics import DqSampleNumericalStatistics
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class UnexpectedNumericalValuesControl(BaseDqControl):
    """Control class for checking unexpected min or max values in sample data."""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.RULE_BASED_CONTROLS_COLUMN_SET

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.UNEXPECTED_NUMERICAL_VALUES

    def get_description(self) -> str:
        return "Unexpected Numerical Values"

    def _execute_control(self) -> List[DqComparisonResult]:
        results = []
        numerical_comp_cols = self.comp_context.get_comparison_cols_by_native_type(ColumnNativeType.Numeric)
        test_group_info = self.comp_context.test_group_info[self.get_test_group_type()]
        for col in numerical_comp_cols:
            col_name = col.column_name
            effective_bmh = min(test_group_info.test_bmh, col.benchmark_horizon)
            max_index = max(len(self.comp_context.control_results) - effective_bmh, 0)
            filtered_controls = list(reversed(self.comp_context.control_results[max_index:]))
            test_stat_collection = self.comp_context.test_calc_result.sample_stats.numerical_statistics
            if len(filtered_controls) > 0 and col_name in test_stat_collection:
                control_min, control_max = self.__get_control_min_max_values(filtered_controls, col_name)
                test_numerical_stats = test_stat_collection[col_name]
                self.__check_unexpected_min(results, test_numerical_stats, control_min, col_name)
                self.__check_unexpected_max(results, test_numerical_stats, control_max, col_name)
        return results

    def __check_unexpected_min(self, results: List[DqComparisonResult],
                               test_numerical_stats: DqSampleNumericalStatistics, control_min_value: float,
                               col_name: str):
        test_min = test_numerical_stats.min
        is_less_than_min = test_min < control_min_value if not math.isnan(control_min_value) else True
        if not math.isnan(test_min) and is_less_than_min:
            result = self._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=col_name,
                result_code=DqComparisonResultCode.UNEXPECTED_MINIMUM,
                property_code="UnexpectedMinimum",
                message=f"The minimum value in the test set ({test_min}) is smaller than the control "
                        f"minimum ({control_min_value}) for the column {col_name}")
            result.property_key_numeric = FormattingHelper.to_nullable(test_min)
            results.append(result)

    def __check_unexpected_max(self, results: List[DqComparisonResult], test_numerical_stats, control_max_value: float,
                               col_name: str):
        test_max = test_numerical_stats.max
        is_higher_than_max = test_max > control_max_value if not math.isnan(control_max_value) else True
        if not math.isnan(test_max) and is_higher_than_max:
            result = self._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=col_name,
                result_code=DqComparisonResultCode.UNEXPECTED_MAXIMUM,
                property_code="TestMaximum",
                message=f"The maximum value in the test set ({test_max}) is greater than the control "
                        f"maximum ({control_max_value}) for the column {col_name}")
            result.property_key_numeric = FormattingHelper.to_nullable(test_max)
            results.append(result)

    @staticmethod
    def __get_control_min_max_values(filtered_controls: List[DqCalculationResult], col_name: str):
        min_values, max_values = [], []
        for control in filtered_controls:
            stat_collection = control.sample_stats.numerical_statistics
            if col_name not in stat_collection:
                continue
            numerical_stats = stat_collection[col_name]
            current_min, current_max = numerical_stats.min, numerical_stats.max
            if not math.isnan(current_min):
                min_values.append(current_min)
            if not math.isnan(current_max):
                max_values.append(current_max)
        if len(min_values) == 0 and len(max_values) == 0:
            return float("nan"), float("nan")

        return min(min_values), max(max_values)
