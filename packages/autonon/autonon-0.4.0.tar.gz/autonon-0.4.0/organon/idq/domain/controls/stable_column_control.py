"""This module includes StableColumnControl class."""
import math
from typing import List, Dict

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.string_helper import is_null_or_empty
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import DqCategoricalStatistics
from organon.idq.domain.businessobjects.statistics.dq_sample_numerical_statistics import DqSampleNumericalStatistics
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class StableColumnControl(BaseDqControl):
    """Class for Stable Column Control."""

    @staticmethod
    def get_control_type() -> DqControlType:
        """:returns control type"""
        return DqControlType.STABLE_COLUMN

    @classmethod
    def get_test_group_type(cls) -> DqTestGroupType:
        """:returns group type of dq control"""
        return DqTestGroupType.RULE_BASED_CONTROLS_COLUMN_SET

    def get_description(self) -> str:
        """:returns description of control"""
        return "Stable Column Control"

    def _execute_control(self) -> List[DqComparisonResult]:
        """:return: list of comparison results"""
        self.__validate_parameters(self.comp_context)

        nominal_comp_cols = self.comp_context.get_nominal_comparison_columns()
        nominal_col_names = [comp_col.column_name for comp_col in nominal_comp_cols]
        sample_nominal_stats = {col: stat for col, stat in
                                self.comp_context.test_calc_result.sample_stats.nominal_statistics.items()
                                if col in nominal_col_names}
        nominal_cardinalities = {stat: sample_nominal_stats[stat].cardinality for stat in sample_nominal_stats}
        nominal_freqs = {stat: sample_nominal_stats[stat].frequencies for stat in sample_nominal_stats}

        sample_numeric_stats = self.comp_context.test_calc_result.sample_stats.numerical_statistics
        numeric_cardinalities = {stat: sample_numeric_stats[stat].cardinality for stat in sample_numeric_stats}
        numeric_freqs = {stat: sample_numeric_stats[stat].frequencies for stat in sample_numeric_stats}

        all_columns_cardinality = numeric_cardinalities
        all_columns_cardinality.update(nominal_cardinalities)
        all_columns_freq = numeric_freqs
        all_columns_freq.update(nominal_freqs)

        results = []
        results.extend(self.__control_cols_for_stability())

        max_cardinality = self.comp_context.comparison_parameters.maximum_nom_cardinality
        min_cardinality = self.comp_context.comparison_parameters.minimum_cardinality
        if max_cardinality is None:
            LogHelper.info("Max cardinality is None, skipping max cardinality control.")
        else:
            if any(column_distinct_count >= max_cardinality for column_distinct_count in
                   nominal_cardinalities.values()):
                results.extend(self.__column_max_cardinality_control(nominal_cardinalities, max_cardinality))

        if min_cardinality is None:
            LogHelper.info("Min cardinality is None, skipping min cardinality control.")
        else:
            if any(column_distinct_count <= min_cardinality for column_distinct_count in
                   all_columns_cardinality.values()):
                results.extend(self.__column_min_cardinality_control(all_columns_cardinality, min_cardinality))
        return results

    @staticmethod
    def __validate_parameters(comp_context):
        if comp_context.test_calc_result is None:
            raise ValueError("T-Calculation result is None.")
        if comp_context.test_calc_result.sample_stats is None:
            raise ValueError("T-Calculation result sample stats is None.")
        if comp_context.test_calc_result.sample_stats.numerical_statistics is None:
            raise ValueError("T-Calculation result numeric sample stats is None.")
        if comp_context.test_calc_result.sample_stats.nominal_statistics is None:
            raise ValueError("T-Calculation result nominal sample stats is None.")
        if comp_context.comparison_parameters is None:
            raise ValueError("T-Calculation comparison parameters is None.")

    def __control_cols_for_stability(self):
        results = []
        sample_numeric_stats = self.comp_context.test_calc_result.sample_stats.numerical_statistics
        for comp_col in self.comp_context.get_comparison_cols_by_native_type(ColumnNativeType.Numeric):
            col = comp_col.column_name
            if comp_col.column_name not in sample_numeric_stats:
                continue
            stats = sample_numeric_stats[col]
            if stats.missing_values is None:
                continue
            self.__control_all_zero(results, col, stats)
            self.__control_numeric_all_null(results, col, stats)
            self.__control_numeric_constant(results, col, stats)

        nominal_stats = self.comp_context.test_calc_result.sample_stats.nominal_statistics
        for comp_col in self.comp_context.get_nominal_comparison_columns():
            if comp_col.column_name in nominal_stats:
                self.__control_nominal_all_null_or_constant(results, comp_col.column_name,
                                                            nominal_stats[comp_col.column_name])
        return results

    def __control_all_zero(self, results: List[DqComparisonResult], col: str, stats: DqSampleNumericalStatistics):
        default_values = stats.missing_values
        default_frequencies = stats.missing_values_frequencies
        if 0 in default_values:
            n_val = stats.n_val
            n_miss = stats.n_miss
            zero_count = default_frequencies[0] if 0 in default_frequencies else 0
            if n_val > 0 and n_val == n_miss and n_val == zero_count:
                comp_result = self._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col,
                    result_code=DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_ZERO,
                    message=f"Column values consist of only zeros for the column: {col}",
                    property_code="ColumnValuesAreAllZero",
                )
                comp_result.property_key_nominal = "true"
                results.append(comp_result)
        else:
            min_val = stats.min
            max_val = stats.max
            if min_val == 0 and max_val == 0:
                comp_result = self._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col,
                    result_code=DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_ZERO,
                    message=f"Non-default column values consist of only zeros for the column: {col}",
                    property_code="ColumnValuesAreAllZero"
                )
                comp_result.property_key_nominal = "true"
                results.append(comp_result)

    def __control_numeric_all_null(self, results: List[DqComparisonResult], col: str,
                                   stats: DqSampleNumericalStatistics):
        default_values = stats.missing_values
        default_frequencies = stats.missing_values_frequencies
        if None in default_values:
            n_val = stats.n_val
            n_miss = stats.n_miss
            nan_count = default_frequencies[None] if None in default_frequencies else 0
            if n_val > 0 and n_val == n_miss and n_val == nan_count:
                comp_result = self._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col,
                    result_code=DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_NULL,
                    message=f"Column values consist of only NULL values for the column: {col}",
                    property_code="ColumnValuesAreAllNull",
                )
                comp_result.property_key_nominal = "true"
                results.append(comp_result)
        else:
            min_val = stats.min
            max_val = stats.max
            if math.isnan(min_val) and math.isnan(max_val):
                comp_result = self._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col,
                    result_code=DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_NULL,
                    message=f"Non-default column values consist of only NULL values for the column: {col}",
                    property_code="ColumnValuesAreAllNull"
                )
                comp_result.property_key_nominal = "true"
                results.append(comp_result)

    def __control_numeric_constant(self, results: List[DqComparisonResult], col: str,
                                   stats: DqSampleNumericalStatistics):
        if stats.cardinality == 1 and stats.frequencies is not None and len(stats.frequencies) == 1:
            single_val = next(iter(stats.frequencies.keys()))
            comp_result = self._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=col,
                result_code=DqComparisonResultCode.COLUMN_IS_CONSTANT,
                message=f"Column consists of a single value ({single_val}) for the column: {col}",
                property_code="ColumnIsConstant"
            )
            comp_result.property_key_nominal = "true"
            results.append(comp_result)

    def __control_nominal_all_null_or_constant(self, results: List[DqComparisonResult], col: str,
                                               stats: DqCategoricalStatistics):
        frequencies = stats.frequencies
        cardinality = len(frequencies)
        if cardinality == 1:
            single_val = next(iter(frequencies.keys()))
            val = str(single_val) if single_val is not None else None
            if is_null_or_empty(val):
                comp_result = self._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col,
                    result_code=DqComparisonResultCode.COLUMN_VALUES_ARE_ALL_NULL,
                    message=f"Column consists of only NULL values for the column: {col}",
                    property_code="ColumnValuesAreAllNull"
                )
                comp_result.property_key_nominal = "true"
                results.append(comp_result)
            else:
                comp_result = self._get_comparison_result(
                    data_entity=DataEntityType.COLUMN,
                    data_entity_name=col,
                    result_code=DqComparisonResultCode.COLUMN_IS_CONSTANT,
                    message=f"Column consists of a single value ({val}) for the column: {col}",
                    property_code="ColumnIsConstant"
                )
                comp_result.property_key_nominal = "true"
                results.append(comp_result)

    @classmethod
    def __column_max_cardinality_control(cls, unique_val_nums_list: Dict[str, int], max_cardinality: int) -> \
            List[DqComparisonResult]:
        results = []
        above_max_cols_names = [col for col, unq_cnt in unique_val_nums_list.items() if unq_cnt >= max_cardinality]
        for col in above_max_cols_names:
            comp_result = cls._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=col,
                result_code=DqComparisonResultCode.CARDINALITY_EXCEEDS_MAXIMUM_CARDINALITY,
                property_code="MaximumCardinalityForTheColumn",
                message=f"Column cardinality is greater than or equal to {max_cardinality} for the column: {col}"
            )
            comp_result.property_key_numeric = max_cardinality
            results.append(comp_result)
        return results

    @classmethod
    def __column_min_cardinality_control(cls, unique_val_nums_list: Dict[str, int], min_cardinality: int) -> \
            List[DqComparisonResult]:
        results = []
        below_min_cols_names = [col for col, unq_cnt in unique_val_nums_list.items() if unq_cnt <= min_cardinality]
        for col in below_min_cols_names:
            comp_result = cls._get_comparison_result(
                data_entity=DataEntityType.COLUMN,
                data_entity_name=col,
                result_code=DqComparisonResultCode.CARDINALITY_IS_BELOW_MINIMUM_THRESHOLD,
                property_code="MinimumCardinalityForTheColumn",
                message=f"Column cardinality is less than or equal to {min_cardinality} for the column: {col}"
            )
            comp_result.property_key_numeric = min_cardinality
            results.append(comp_result)
        return results
