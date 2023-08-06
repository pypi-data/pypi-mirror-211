"""Includes UnexpectedNominalValuesControl class."""
from typing import List, Set

from organon.fl.core.helpers.string_helper import is_null_or_empty
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import DqCategoricalStatistics
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class UnexpectedNominalValuesControl(BaseDqControl):
    """Control class for checking unexpected nominal values in data."""

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        return DqTestGroupType.RULE_BASED_CONTROLS_COLUMN_SET

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.UNEXPECTED_NOMINAL_VALUES

    def get_description(self) -> str:
        return "Unexpected Nominal Values"

    def _execute_control(self) -> List[DqComparisonResult]:
        results = []
        nominal_comp_cols = self.comp_context.get_nominal_comparison_columns()
        test_group_info = self.comp_context.test_group_info[self.get_test_group_type()]
        for col in nominal_comp_cols:
            col_name = col.column_name
            effective_bmh = min(test_group_info.test_bmh, col.benchmark_horizon)
            max_index = max(len(self.comp_context.control_results) - effective_bmh, 0)
            filtered_controls = list(reversed(self.comp_context.control_results[max_index:]))
            test_stat_collection = self.comp_context.test_calc_result.population_stats.nominal_statistics
            if test_stat_collection is None:
                LogHelper.info("Test statistics collection is null, column values tests skipped")
            elif len(filtered_controls) > 0 and col_name in test_stat_collection:
                union_of_control_values = self.__get_control_values(filtered_controls, col_name)
                test_nominal_stats = test_stat_collection[col_name]
                test_values = set(UnexpectedNominalValuesControl.__get_unique_values(test_nominal_stats))
                unexpected_values = list(test_values - union_of_control_values)
                results.extend(self.__get_unexpected_values_results(unexpected_values, col_name))
        return results

    def __get_unexpected_values_results(self, unexpected_values: List[str], column: str):
        msg = f"Following unexpected values are found the first time in data for the column {column}: "
        msg += "\n".join([val if not is_null_or_empty(val) else "NULL" for val in unexpected_values])
        results = []
        for val in unexpected_values:
            result = DqComparisonResult(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=column,
                test_group=self.get_test_group_type(),
                result_code=DqComparisonResultCode.UNEXPECTED_NOMINAL_VALUES,
                property_code="UnexpectedValues",
                message=msg
            )
            result.property_key_nominal = val
            results.append(result)
        return results

    @staticmethod
    def __get_control_values(filtered_controls: List[DqCalculationResult], col_name: str) -> Set[str]:
        union_of_control_values: Set[str] = set()
        for control in filtered_controls:
            control_stats_collection = control.population_stats.nominal_statistics
            if col_name not in control_stats_collection:
                continue
            union_of_control_values.update(UnexpectedNominalValuesControl.__get_unique_values(
                control_stats_collection[col_name]))
        return union_of_control_values

    @staticmethod
    def __get_unique_values(categorical_stats: DqCategoricalStatistics):
        return [str(key) if key is not None else None for key in categorical_stats.frequencies.keys()]
