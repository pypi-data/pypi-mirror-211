"""Includes PsiNominalSignalControl class."""
from typing import List, Dict

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.idq.core.dq_constants import DqConstants
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import DqCategoricalStatistics
from organon.idq.domain.controls.base_psi_signal_control import BasePsiSignalControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.signal_type import SignalType
from organon.idq.domain.helpers.statistics.dq_statistical_functions import DqStatisticalFunctions


class PsiNominalSignalControl(BasePsiSignalControl):
    """Control class psi comparison for nominal column"""

    @staticmethod
    def get_control_type() -> DqControlType:
        return DqControlType.PSI_NOMINAL_VALUES

    def get_description(self) -> str:
        return "Psi Nominal Signals"

    def _execute_control(self) -> List[DqComparisonResult]:
        results = []
        nominal_comp_cols = self.comp_context.get_nominal_comparison_columns()
        test_group_info = self.comp_context.test_group_info[self.get_test_group_type()]
        for col in nominal_comp_cols:
            col_name = col.column_name
            filtered_controls = self._get_filtered_columns(col, test_group_info)
            test_nominal_stat_collection = self.comp_context.test_calc_result.population_stats.nominal_statistics
            if test_nominal_stat_collection is None:
                LogHelper.info("Test statistics collection is null, psi tests skipped")

            elif len(filtered_controls) > 0 and col_name in test_nominal_stat_collection:
                test_nominal_stats = test_nominal_stat_collection[col_name]
                self.__control_executor(test_nominal_stats, filtered_controls, col_name, results)

        return results

    def __control_executor(self, test_nominal_stats: DqCategoricalStatistics,
                           filtered_controls: List[DqCalculationResult], col_name: str,
                           results: List[DqComparisonResult]):
        test_frequencies = test_nominal_stats.frequencies
        max_psi = 0.0
        maximum_psi_sample = ""
        maximum_psi_category = ""
        maximum_psi_control_set_frequencies: Dict[str, float] = {}
        psi_per_control_set: Dict[str, float] = {}
        for control in filtered_controls:
            stat_collection = control.population_stats.nominal_statistics
            if col_name not in stat_collection:
                continue
            nominal_stats = stat_collection[col_name]
            control_frequencies = nominal_stats.frequencies
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
                maximum_psi_control_set_frequencies = {str(key): value for (key, value) in
                                                       control_frequencies.items()}
        psi_signal = self.get_signal_type(max_psi)
        if psi_signal == SignalType.GREEN:
            return
        result_code = DqComparisonResultCode.PSI_RED_SIGNAL if psi_signal == SignalType.RED \
            else DqComparisonResultCode.PSI_YELLOW_SIGNAL
        self.check_maximum_psi(col_name, result_code, results, max_psi, "MaximumPsi")
        self.check_maximum_psi_control_set(col_name, result_code, results, maximum_psi_sample,
                                           "MaximumPsiControlSet")
        self.check_maximum_psi_category(col_name, result_code, results, maximum_psi_category,
                                        "MaximumPsiCategory")
        self.check_test_frequency(col_name, result_code, results, test_frequencies,
                                  "NominalColumnTestFrequencies")
        self.check_max_psi_control_frequency(col_name, result_code, results,
                                             maximum_psi_control_set_frequencies,
                                             "NominalColumnMaximumPsiControlFrequencies")
        self.check_psi_per_control_set(col_name, result_code, results, psi_per_control_set,
                                       "PsiPerControlSet")
