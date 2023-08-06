"""Includes PsiNumericSignalControl class."""
from typing import List, Dict

from organon.fl.core.collections.sorted_dict import SortedDict
from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.fl.mathematics.businessobjects.sets.interval import Interval
from organon.idq.core.dq_constants import DqConstants
from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.statistics.dq_sample_numerical_statistics import DqSampleNumericalStatistics
from organon.idq.domain.controls.base_psi_signal_control import BasePsiSignalControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.signal_type import SignalType
from organon.idq.domain.helpers.statistics.dq_statistical_functions import DqStatisticalFunctions


class PsiNumericSignalControl(BasePsiSignalControl):
    """Control class psi comparison for numeric column"""

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.PSI_NUMERIC_VALUES

    def get_description(self) -> str:
        return "Psi Numeric Signals"

    def _execute_control(self) -> List[DqComparisonResult]:
        if self.comp_context.test_calc_parameters.is_existing_calculation and \
                self.comp_context.test_calc_result.sample_data is None:
            LogHelper.warning("Will not execute PSI control for numeric columns since test calculation "
                              "is given as existing calculation with dataframe source")
            return []
        numeric_comp_cols = self.comp_context.get_comparison_cols_by_native_type(ColumnNativeType.Numeric)
        sample_data = self.comp_context.test_calc_result.sample_data
        results = []
        test_group_info = self.comp_context.test_group_info[self.get_test_group_type()]
        for col in numeric_comp_cols:
            col_name = col.column_name
            filtered_controls = self._get_filtered_columns(col, test_group_info)
            if len(filtered_controls) > 0 and col_name in sample_data.data_frame.columns:
                test_array = sample_data.data_frame[col_name]
                self.__control_executor(test_array, filtered_controls, col_name, results)

        return results

    def __control_executor(self, test_array,
                           filtered_controls: List[DqCalculationResult], col_name: str,
                           results: List[DqComparisonResult]):
        max_psi = 0.0
        maximum_psi_sample, maximum_psi_category = "", ""
        maximum_psi_control_frequencies: SortedDict[str, float] = SortedDict()
        maximum_psi_test_frequencies: SortedDict[str, float] = SortedDict()
        default_value_string = "A000001"
        non_default_value_string = "B000001"
        psi_per_control_set: Dict[str, float] = {}
        for control in filtered_controls:
            stat_collection = control.sample_stats.numerical_statistics
            if col_name not in stat_collection:
                continue
            control_stats = stat_collection[col_name]
            control_frequencies = self._get_control_frequencies(control_stats, default_value_string,
                                                                non_default_value_string)
            test_frequencies = self._get_test_frequencies(control_stats, default_value_string,
                                                          non_default_value_string, test_array)
            psi_tuple = DqStatisticalFunctions.population_stability_index(control_frequencies,
                                                                          test_frequencies,
                                                                          DqConstants.MINIMUM_INJECTION)
            psi_value = psi_tuple[1]
            sample_to_string = control.calculation_name
            psi_per_control_set[sample_to_string] = psi_value
            if psi_value > max_psi:
                max_psi = psi_value
                maximum_psi_sample = sample_to_string
                maximum_psi_category = psi_tuple[0]
                maximum_psi_control_frequencies = control_frequencies
                maximum_psi_test_frequencies = test_frequencies
        psi_signal = self.get_signal_type(max_psi)
        if psi_signal == SignalType.GREEN:
            return
        result_code = DqComparisonResultCode.PSI_RED_SIGNAL if psi_signal == SignalType.RED \
            else DqComparisonResultCode.PSI_YELLOW_SIGNAL
        self.__check_psi_signal(col_name, result_code, results, psi_signal, "PsiSignal")
        self.check_maximum_psi(col_name, result_code, results, max_psi, "MaximumPsi")
        self.check_maximum_psi_category(col_name, result_code, results, maximum_psi_category,
                                        "MaximumPsiCategory")
        self.check_maximum_psi_category(col_name, result_code, results, maximum_psi_category,
                                        "MaximumPsiInterval")
        self.check_maximum_psi_control_set(col_name, result_code, results, maximum_psi_sample,
                                           "MaximumPsiControlSet")
        self.check_test_frequency(col_name, result_code, results, maximum_psi_test_frequencies,
                                  "NumericalColumnTestFrequencies")
        self.check_max_psi_control_frequency(col_name, result_code, results,
                                             maximum_psi_control_frequencies,
                                             "NumericalColumnMaximumPsiControlFrequencies")
        self.check_psi_per_control_set(col_name, result_code, results, psi_per_control_set,
                                       "PsiPerControlSet")

    def __check_psi_signal(self, col_name: str, result_code: DqComparisonResultCode,
                           results: List[DqComparisonResult], psi_signal: SignalType, property_key: str):
        result = DqComparisonResult(
            data_entity=DataEntityType.COLUMN,
            data_entity_name=col_name,
            test_group=self.get_test_group_type(),
            result_code=result_code,
            property_code=property_key,
            message=f"Distribution is unstable for the numeric column {col_name}")
        result.property_key_nominal = psi_signal.name
        results.append(result)

    @staticmethod
    def _get_control_frequencies(control_stats: DqSampleNumericalStatistics,
                                 default_value_string: str, non_default_value_string: str) -> SortedDict[str, float]:

        default_value_frequencies = control_stats.missing_values_frequencies
        default_values_count = 0.0
        if default_value_frequencies is not None:
            default_values_count = sum(default_value_frequencies.values())
        result: SortedDict[str, float] = SortedDict()
        result[default_value_string] = default_values_count
        interval_statistics = control_stats.interval_statistics
        if interval_statistics is None:
            result[non_default_value_string] = 0
        else:
            for interval_statistic_key, interval_statistic_value in interval_statistics.items():
                interval_frequency = interval_statistic_value.count
                result[interval_statistic_key.to_string()] = interval_frequency
        return result

    @staticmethod
    def _get_test_frequencies(control_stats: DqSampleNumericalStatistics,
                              default_value_string: str, non_default_value_string: str, test_array) \
            -> SortedDict[str, float]:
        interval_statistics = control_stats.interval_statistics
        upper_bounds_map: SortedDict[float, Interval] = SortedDict()
        test_normal_values: SortedDict[float, float] = SortedDict()
        if interval_statistics is not None:
            for interval_statistic_key in interval_statistics:
                upper_bounds_map[interval_statistic_key.upper_bound] = interval_statistic_key
                test_normal_values[interval_statistic_key.upper_bound] = 0.0

        default_values = control_stats.missing_values if control_stats.missing_values is not None else []
        default_value_count = 0.0
        for value in test_array:
            if value in default_values:
                default_value_count = default_value_count + 1
            else:
                for upper_bound_key in upper_bounds_map:
                    if value <= upper_bound_key:
                        test_normal_values[upper_bound_key] = test_normal_values[upper_bound_key] + 1
                        break

        result: SortedDict[str, float] = SortedDict()
        result[default_value_string] = default_value_count
        if interval_statistics is None:
            result[non_default_value_string] = len(test_array) - default_value_count
        else:
            for test_normal_values_key, test_normal_values_value in test_normal_values.items():
                result[(upper_bounds_map[test_normal_values_key]).to_string()] = test_normal_values_value
        return result
