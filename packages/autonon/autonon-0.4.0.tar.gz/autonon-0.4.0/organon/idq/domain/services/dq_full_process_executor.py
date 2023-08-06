"""todo"""
from typing import List, Optional, Dict, Tuple

from organon.idq.domain.businessobjects.dq_calculation_output import DqCalculationOutput
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.main_sample_results import MainSampleResults
from organon.idq.domain.businessobjects.record_sources.dq_df_record_source import DqDfRecordSource
from organon.idq.domain.enums.dq_control_type import DqControlType
from organon.idq.domain.enums.dq_run_type import DqRunType
from organon.idq.domain.reporting.dq_reporting_executor import DqReportingExecutor
from organon.idq.domain.reporting.objects.base_dq_output_report import BaseDqOutputReport
from organon.idq.domain.services.task_executor.calculation.dq_calculation_task_executor import DqCalculationTaskExecutor
from organon.idq.domain.services.task_executor.comparison.dq_comparison_task_executor import DqComparisonTaskExecutor
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.abstractions.dq_full_process_input import DqFullProcessInput
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo


class DqFullProcessExecutor:
    """todo"""

    def __init__(self, dq_settings: DqFullProcessInput):
        self.dq_settings = dq_settings
        self._run_type = self._get_run_type()

    def execute(self) -> Tuple[BaseDqOutputReport, List[DqCalculationOutput]]:
        """todo"""
        calculation_results = self._get_calculation_results()
        self.__decide_comparison_columns(calculation_results[-1])
        comparison_output = self._run_controls(calculation_results)
        report = self._generate_reports(comparison_output.comparison_results, calculation_results)
        calculation_outputs = self._get_dq_calculation_outputs(calculation_results)
        return report, calculation_outputs

    def _get_dq_calculation_outputs(self, calculation_results: List[DqCalculationResult]) -> List[DqCalculationOutput]:
        outputs = []
        for i, res in enumerate(calculation_results):
            output = DqCalculationOutput()
            output.calculation_result = res
            res.sample_data = None
            calc_params = self.dq_settings.calculation_parameters[i]
            source = calc_params.input_source_settings.source
            if isinstance(source, DqDfRecordSource):
                source.locator = None
            output.calculation_parameters = self.dq_settings.calculation_parameters[i]
            outputs.append(output)
        return outputs

    def _get_calculation_results(self) -> List[DqCalculationResult]:
        """todo"""
        results = []
        for i, calc in enumerate(self.dq_settings.calculation_parameters):
            is_t_calc = i == len(self.dq_settings.calculation_parameters) - 1  # for t_calc get sample data
            executor = self._get_calculation_task_executor(calc, is_t_calc)
            result = executor.execute()
            result.calculation_name = calc.calculation_name
            results.append(result)
        return results

    def _get_calculation_task_executor(self, calculation_parameters: DqBaseCalculationParameters,
                                       is_t_calculation: bool) \
            -> DqCalculationTaskExecutor:
        return DqCalculationTaskExecutor(calculation_parameters,
                                         run_type=self._run_type, is_test_calculation=is_t_calculation)

    def _run_controls(self, calculation_results: List[DqCalculationResult]) -> MainSampleResults:
        """Runs dq controls on sample data."""
        comparison_executor = self._get_comparison_task_executor(calculation_results)
        comparison_output = comparison_executor.execute()
        return comparison_output

    def _get_comparison_task_executor(self, calculation_results: List[DqCalculationResult]) -> DqComparisonTaskExecutor:
        return DqComparisonTaskExecutor(self.dq_settings.comparison_parameters,
                                        self.dq_settings.calculation_parameters,
                                        calculation_results,
                                        control_types_to_execute=self._get_controls_to_execute())

    def _generate_reports(self, comparison_results: List[DqComparisonResult],
                          calculation_results: List[DqCalculationResult]) -> BaseDqOutputReport:
        """Generates reports from dq comparison results."""
        report_helper = self._get_report_helper(comparison_results, calculation_results)
        report = report_helper.execute()
        return report

    def _get_report_helper(self, comparison_results: List[DqComparisonResult],
                           calculation_results: List[DqCalculationResult]):
        return DqReportingExecutor(self.dq_settings, calculation_results, comparison_results,
                                   self._run_type)

    def _get_controls_to_execute(self) -> Optional[List[DqControlType]]:
        """:returns: controls for run type"""
        common_tests = [DqControlType.EMPTY_TABLE, DqControlType.STABLE_COLUMN, DqControlType.DUPLICATE_KEYS]
        if self._run_type == DqRunType.RUN_ONE_DATA_SOURCE:
            return common_tests
        return common_tests + [DqControlType.UNEXPECTED_NUMERICAL_VALUES, DqControlType.TABLE_COLUMNS,
                               DqControlType.UNEXPECTED_NOMINAL_VALUES, DqControlType.COLUMN_MEAN,
                               DqControlType.DATA_SOURCE_STATS_TL_CONTROL,
                               DqControlType.DATA_SOURCE_STATS_TIME_SERIES_CONTROL, DqControlType.PSI_NOMINAL_VALUES,
                               DqControlType.PSI_NUMERIC_VALUES]

    def _get_run_type(self) -> DqRunType:
        # todo
        if len(self.dq_settings.calculation_parameters) == 1:
            return DqRunType.RUN_ONE_DATA_SOURCE
        return DqRunType.RUN_ONE_DATA_SOURCE_WITH_PARTITIONS

    def __decide_comparison_columns(self, t_calc_result: DqCalculationResult):
        comp_cols_dict: Dict[str, DqComparisonColumnInfo] = \
            {col.column_name: col for col in self.dq_settings.comparison_parameters.comparison_columns}
        meta_dict: Dict[str, DqColumnMetadata] = {col.column_name: col for col in t_calc_result.column_metadata_list}
        duplicate_column_control_default = False
        bh_default = len(self.dq_settings.calculation_parameters) - 1
        for col in t_calc_result.data_source_stats.data_column_collection:
            if col.column_name in meta_dict and meta_dict[col.column_name].inclusion_flag:
                if col.column_name in comp_cols_dict:
                    comp_col = comp_cols_dict[col.column_name]
                    comp_col.duplicate_column_control = duplicate_column_control_default \
                        if comp_col.duplicate_column_control is None else comp_col.duplicate_column_control
                    bh_value = comp_col.benchmark_horizon
                    comp_col.benchmark_horizon = bh_default if bh_value is None or bh_value > bh_default else bh_value
                else:
                    new_comp_col = DqComparisonColumnInfo()
                    new_comp_col.column_name = col.column_name
                    new_comp_col.duplicate_column_control = duplicate_column_control_default
                    new_comp_col.benchmark_horizon = bh_default
                    comp_cols_dict[col.column_name] = new_comp_col
            else:
                if col.column_name in comp_cols_dict:
                    comp_cols_dict.pop(col.column_name)
        self.dq_settings.comparison_parameters.comparison_columns = list(comp_cols_dict.values())
