"""Includes DqCalculationTaskExecutor class."""
from typing import List

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.idq.dataaccess.record_source_reader import RecordSourceReader
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.businessobjects.dq_data_source import DqDataSource
from organon.idq.domain.businessobjects.statistics.data_source_statistics import DataSourceStatistics
from organon.idq.domain.businessobjects.statistics.population_statistics import PopulationStatistics
from organon.idq.domain.businessobjects.statistics.sample_statistics import SampleStatistics
from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType
from organon.idq.domain.enums.dq_run_type import DqRunType
from organon.idq.domain.services.statistics.source_statistics.df_source_stats_service import DfSourceStatsService
from organon.idq.domain.services.statistics.source_statistics.dq_source_stats_base_service import \
    DqSourceStatsBaseService
from organon.idq.domain.services.statistics.source_statistics.file_source_stats_service import FileSourceStatsService
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.calculation.dq_df_calculation_parameters import DqDfCalculationParameters
from organon.idq.domain.settings.calculation.dq_file_calculation_parameters import DqFileCalculationParameters
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata


class DqCalculationTaskExecutor:
    """Executes dq calculations with given parameters"""

    def __init__(self, calculation_parameters: DqBaseCalculationParameters,
                 run_type: DqRunType, is_test_calculation: bool = False):
        self.calculation_parameters: DqBaseCalculationParameters = calculation_parameters
        self.stats_service: DqSourceStatsBaseService = self._get_stats_service()
        self.is_test_calculation = is_test_calculation
        self.run_type = run_type

    def execute(self) -> DqCalculationResult:
        """Starts dq calculations"""
        if self.calculation_parameters.is_existing_calculation:
            return self._execute_for_existing_calculation()
        return self._execute_for_normal_calculation()

    def _execute_for_normal_calculation(self) -> DqCalculationResult:
        result = DqCalculationResult()
        result.calculation_name = self.calculation_parameters.calculation_name
        result.data_source_stats = DataSourceStatistics()
        result.population_stats = PopulationStatistics()

        sample_data = self._get_sample_data()
        data_col_collection = self._get_data_column_collection(sample_data)
        self._update_params_with_column_collection(data_col_collection)
        sample_stats = self._compute_sample_stats(sample_data, data_col_collection)
        filtered_columns = self._filter_high_cardinality_columns(data_col_collection)
        population_nominal_stats = self._get_population_nominal_stats(filtered_columns, data_col_collection)
        columns_metadata_list = self._update_params_with_column_collection(data_col_collection)

        result.data_source_stats.data_column_collection = data_col_collection
        result.data_source_stats.row_count = sample_data.full_data_row_count
        result.sample_stats = sample_stats
        result.column_metadata_list = columns_metadata_list
        result.population_stats.nominal_statistics = population_nominal_stats

        if self.is_test_calculation:
            result.sample_data = DataFrame()
            result.sample_data.data_frame = sample_data.sampled_data

        return result

    def _execute_for_existing_calculation(self) -> DqCalculationResult:
        if self.is_test_calculation:
            if self.calculation_parameters.input_source_settings.source.get_type() != DqRecordSourceType.DATA_FRAME:
                sample_data = self._get_sample_data()
                self.calculation_parameters.existing_result.sample_data = DataFrame()
                self.calculation_parameters.existing_result.sample_data.data_frame = sample_data.sampled_data
        return self.calculation_parameters.existing_result

    def _get_data_column_collection(self, sample_data: DqDataSource) -> DqDataColumnCollection:
        columns_dq_metadata = self.calculation_parameters.column_dq_metadata_list
        return self.stats_service.get_data_column_collection(sample_data, columns_dq_metadata)

    def _get_sample_data(self) -> DqDataSource:
        record_source_reader = RecordSourceReader(self.calculation_parameters.input_source_settings)
        return record_source_reader.read()

    def _compute_sample_stats(self, sample_data: DqDataSource, data_column_collection: DqDataColumnCollection) \
            -> SampleStatistics:
        return self.stats_service.get_sample_stats(sample_data.sampled_data, data_column_collection)

    def _update_params_with_column_collection(self, data_column_collection: DqDataColumnCollection) \
            -> List[DqColumnMetadata]:
        return self.stats_service.update_calc_params(data_column_collection)

    def _filter_high_cardinality_columns(self, data_column_collection: DqDataColumnCollection) -> List[str]:
        return self.stats_service.filter_high_cardinality_columns(data_column_collection)

    def _get_population_nominal_stats(self, filtered_columns: List[str],
                                      data_column_collection: DqDataColumnCollection):
        return self.stats_service.get_population_nominal_statistics(filtered_columns, data_column_collection)

    def _get_stats_service(self):

        if isinstance(self.calculation_parameters, DqFileCalculationParameters):
            return FileSourceStatsService(self.calculation_parameters)
        if isinstance(self.calculation_parameters, DqDfCalculationParameters):
            return DfSourceStatsService(self.calculation_parameters)
        raise NotImplementedError
