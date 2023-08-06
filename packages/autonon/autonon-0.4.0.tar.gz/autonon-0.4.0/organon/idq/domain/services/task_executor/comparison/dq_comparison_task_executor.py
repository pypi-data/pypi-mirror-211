"""todo"""
from typing import List

from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_control_parameters import DqControlParameters
from organon.idq.domain.businessobjects.main_sample_results import MainSampleResults
from organon.idq.domain.controls.base_dq_control import BaseDqControl
from organon.idq.domain.controls.column_mean_control import ColumnMeanControl
from organon.idq.domain.controls.data_source_stats_time_series_control import DataSourceStatsTimeSeriesControl
from organon.idq.domain.controls.data_source_stats_traffic_light_control import DataSourceStatsTrafficLightControl
from organon.idq.domain.controls.duplicate_keys_control import DuplicateKeysControl
from organon.idq.domain.controls.empty_table_control import EmptyTableControl
from organon.idq.domain.controls.psi_nominal_signal_control import PsiNominalSignalControl
from organon.idq.domain.controls.psi_numeric_signal_control import PsiNumericSignalControl
from organon.idq.domain.controls.stable_column_control import StableColumnControl
from organon.idq.domain.controls.table_columns_control import TableColumnsControl
from organon.idq.domain.controls.unexpected_nominal_values_control import UnexpectedNominalValuesControl
from organon.idq.domain.controls.unexpected_numerical_values_control import UnexpectedNumericalValuesControl
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.abstractions.dq_base_comparison_parameters import DqBaseComparisonParameters


class DqComparisonTaskExecutor:
    """todo"""

    def __init__(self, comparison_parameters: DqBaseComparisonParameters,
                 calculation_parameters: List[DqBaseCalculationParameters],
                 calculation_results: List[DqCalculationResult],
                 control_types_to_execute: List[DqControlType] = None):
        self.dq_control_params: DqControlParameters = self.__initialize_params(comparison_parameters,
                                                                               calculation_parameters,
                                                                               calculation_results)
        self.controls_to_execute = self.__get_control_classes_to_execute(control_types_to_execute)

    @classmethod
    def get_control_classes(cls):
        """Returns all control classes for executor"""
        return [TableColumnsControl, EmptyTableControl, StableColumnControl, UnexpectedNumericalValuesControl,
                UnexpectedNominalValuesControl, DuplicateKeysControl, ColumnMeanControl,
                DataSourceStatsTrafficLightControl, DataSourceStatsTimeSeriesControl, PsiNominalSignalControl,
                PsiNumericSignalControl]

    @classmethod
    def __get_control_classes_to_execute(cls, control_types: List[DqControlType]):
        if control_types is None:
            return cls.get_control_classes().copy()
        return [control_class for control_class in cls.get_control_classes()
                if control_class.get_control_type() in control_types]

    @staticmethod
    def __initialize_params(comparison_parameters: DqBaseComparisonParameters,
                            calculation_parameters: List[DqBaseCalculationParameters],
                            calculation_results: List[DqCalculationResult]):

        control_params = DqControlParameters()
        control_params.comparison_parameters = comparison_parameters
        if len(calculation_results) == 0:
            raise ValueError("Calculations cannot be empty")
        if len(calculation_parameters) != len(calculation_results):
            raise ValueError("Calculation parameters and results lists should be same length")
        control_params.control_results = calculation_results[:-1]
        control_params.control_parameters = calculation_parameters[:-1]
        control_params.test_calc_parameters = calculation_parameters[-1]
        control_params.test_calc_result = calculation_results[-1]
        control_params.test_group_info = {group.group_type: group for group in comparison_parameters.test_groups}
        return control_params

    def execute(self) -> MainSampleResults:
        """todo"""
        results = self.execute_sequentially()
        output = MainSampleResults()
        output.comparison_results = results
        return output

    def execute_sequentially(self):
        """todo"""
        results = []
        for control_class in self.controls_to_execute:
            control = control_class(self.dq_control_params)
            results.extend(self.__execute_control(control))
        return results

    def __execute_control(self, control: BaseDqControl) -> List[DqComparisonResult]:
        test_group_info = self.dq_control_params.test_group_info[control.get_test_group_type()]
        if test_group_info.inclusion_flag is False:
            return []
        return control.execute()
