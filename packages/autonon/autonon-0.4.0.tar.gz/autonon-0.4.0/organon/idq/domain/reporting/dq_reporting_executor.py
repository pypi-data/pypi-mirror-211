"""Includes DqReportingExecutor class."""
from typing import List, Dict

from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.businessobjects.statistics.data_source_statistics import DataSourceStatistics
from organon.idq.domain.businessobjects.statistics.population_statistics import PopulationStatistics
from organon.idq.domain.businessobjects.statistics.sample_statistics import SampleStatistics
from organon.idq.domain.enums.dq_run_type import DqRunType
from organon.idq.domain.reporting.objects.base_dq_output_report import BaseDqOutputReport
from organon.idq.domain.reporting.objects.single_source_report_helper_params import SingleSourceReportHelperParams
from organon.idq.domain.reporting.objects.source_with_partitions_report_helper_params import \
    SourceWithPartitionsReportHelperParams
from organon.idq.domain.reporting.single_source_report_helper import SingleSourceReportHelper
from organon.idq.domain.reporting.source_with_partitions_report_helper import SourceWithPartitionsReportHelper
from organon.idq.domain.settings.abstractions.dq_full_process_input import DqFullProcessInput


class DqReportingExecutor:
    """Class for execute idq reporting"""

    def __init__(self, full_process_input: DqFullProcessInput, calculation_results: List[DqCalculationResult],
                 comparison_results: List[DqComparisonResult], run_type: DqRunType):
        self.full_process_input = full_process_input
        self.calculation_results = calculation_results
        self.comparison_results = comparison_results
        self.run_type = run_type
        self.t_calc_data_source_name = self.full_process_input.calculation_parameters[
            -1].input_source_settings.source.get_name()
        self.t_calc_col_collection = self.__get_t_calc_data_column_collection()
        self.sample_statistics = self.__get_sample_statistics_dict()
        self.population_statistics = self.__get_population_statistics_dict()
        self.data_source_statistics = self.__get_data_source_statistics_dict()

    def execute(self) -> BaseDqOutputReport:
        """
        Execute the relevant reporting service
        """
        t_calc_partition = self.full_process_input.calculation_parameters[-1].input_source_settings.partition_info_list
        filter_str = self._get_filter_str()
        if self.run_type == DqRunType.RUN_ONE_DATA_SOURCE:
            one_df_dq_report_params = SingleSourceReportHelperParams(self.t_calc_data_source_name,
                                                                     self.comparison_results,
                                                                     self.t_calc_col_collection, self.run_type,
                                                                     partition=t_calc_partition)
            one_df_dq_report_params.filter_str = filter_str
            reporting_helper = SingleSourceReportHelper(one_df_dq_report_params)
        elif self.run_type == DqRunType.RUN_ONE_DATA_SOURCE_WITH_PARTITIONS:
            one_df_with_date_dq_report_params = self._get_source_with_date_report_helper_params()
            reporting_helper = SourceWithPartitionsReportHelper(one_df_with_date_dq_report_params)
        else:
            raise NotImplementedError
        return reporting_helper.execute()

    def _get_source_with_date_report_helper_params(self):
        filter_str = self._get_filter_str()
        t_calc_partition = self.full_process_input.calculation_parameters[-1].input_source_settings.partition_info_list
        one_df_with_date_dq_report_params = SourceWithPartitionsReportHelperParams(self.t_calc_data_source_name,
                                                                                   self.comparison_results,
                                                                                   self.t_calc_col_collection,
                                                                                   self.run_type,
                                                                                   partition=t_calc_partition
                                                                                   )
        one_df_with_date_dq_report_params.calculation_count = len(self.calculation_results)
        one_df_with_date_dq_report_params.comparison_column_info = \
            self.full_process_input.comparison_parameters.comparison_columns
        one_df_with_date_dq_report_params.sample_statistics = self.sample_statistics
        one_df_with_date_dq_report_params.population_statistics = self.population_statistics
        one_df_with_date_dq_report_params.data_source_statistics = self.data_source_statistics
        one_df_with_date_dq_report_params.filter_str = filter_str
        return one_df_with_date_dq_report_params

    def _get_filter_str(self) -> str:
        filter_callable = self.full_process_input.calculation_parameters[-1].input_source_settings.filter_callable
        if filter_callable is not None:
            return filter_callable.__name__
        return None

    def __get_sample_statistics_dict(self) -> Dict[str, SampleStatistics]:
        sample_statistics_dict = {}
        for calculation in self.calculation_results:
            sample_statistics_dict[calculation.calculation_name] = calculation.sample_stats

        return sample_statistics_dict

    def __get_population_statistics_dict(self) -> Dict[str, PopulationStatistics]:
        population_statistics_dict = {}
        for calculation in self.calculation_results:
            population_statistics_dict[calculation.calculation_name] = calculation.population_stats
        return population_statistics_dict

    def __get_data_source_statistics_dict(self) -> Dict[str, DataSourceStatistics]:
        data_source_statistics = {}
        for calculation in self.calculation_results:
            data_source_statistics[calculation.calculation_name] = calculation.data_source_stats

        return data_source_statistics

    def __get_t_calc_data_column_collection(self):
        t_calc_results = self.calculation_results[-1]
        data_column_collection_t = t_calc_results.data_source_stats.data_column_collection
        new_data_col_collection = DqDataColumnCollection()
        for col in data_column_collection_t:
            new_data_col_collection.add(col)

        for calculation_result in self.calculation_results[:-1]:
            for data_column in calculation_result.data_source_stats.data_column_collection:
                if new_data_col_collection.get_column(data_column.column_name) is None:
                    new_data_col_collection.add(data_column)
        return new_data_col_collection
