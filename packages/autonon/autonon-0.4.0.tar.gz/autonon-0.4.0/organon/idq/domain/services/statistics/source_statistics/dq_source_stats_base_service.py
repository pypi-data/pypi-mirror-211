"""todo"""

import abc
import math
from typing import Dict, TypeVar, Generic, List

import pandas as pd

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import list_helper
from organon.idq.domain.businessobjects.data_column.dq_data_column import DqDataColumn
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.businessobjects.dq_data_source import DqDataSource
from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import DqCategoricalStatistics
from organon.idq.domain.businessobjects.statistics.sample_statistics import SampleStatistics
from organon.idq.domain.services.statistics.dq_statistics_domain_service import DqStatisticsDomainService
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata

DqCalcParamsType = TypeVar("DqCalcParamsType", bound=DqBaseCalculationParameters)


class DqSourceStatsBaseService(Generic[DqCalcParamsType], metaclass=abc.ABCMeta):
    """todo"""

    def __init__(self, calc_params: DqCalcParamsType):
        self.calc_params: DqCalcParamsType = calc_params

    @abc.abstractmethod
    def get_data_column_collection(self, data_source: DqDataSource, columns_dq_metadata: List[DqColumnMetadata]) \
            -> DqDataColumnCollection:
        """Generates DqDataColumnCollection instance by acquiring column info from data source and metadata settings"""

    def filter_high_cardinality_columns(self, data_column_collection: DqDataColumnCollection) -> List[str]:
        """todo"""
        col_names = [col.column_name for col in data_column_collection if col.column_native_type
                     in self.calc_params.nominal_column_types]
        included_columns = self.calc_params.input_source_settings.included_columns
        if not list_helper.is_null_or_empty(included_columns):
            col_names = [col for col in col_names if col in included_columns]
        if len(col_names) == 0:
            return []
        cardinality_dict = self._get_column_cardinalities_from_population(col_names)
        return [col for col, cardinality in cardinality_dict.items()
                if cardinality <= self.calc_params.max_nominal_cardinality_count]

    @abc.abstractmethod
    def _get_column_cardinalities_from_population(self, column_names: List[str]) -> Dict[str, int]:
        pass

    def get_population_nominal_statistics(self, nominal_column_names: List[str],
                                          data_col_collection: DqDataColumnCollection) \
            -> Dict[str, DqCategoricalStatistics]:
        """Get statistics for nominal columns in data"""

        filtered_metadata = [col_meta for col_meta in self.calc_params.column_dq_metadata_list
                             if col_meta.inclusion_flag and col_meta.column_name in nominal_column_names]
        dq_columns = {col.column_name: col for col in data_col_collection
                      if col.column_name in [meta.column_name for meta in filtered_metadata]}
        all_stats = {}
        histograms = {}
        if len(dq_columns) > 0:
            histograms = self._get_histograms_for_columns(dq_columns)
        for col_meta in filtered_metadata:
            col_name = col_meta.column_name
            missing_values = col_meta.default_values
            stats = DqCategoricalStatistics(missing_values)
            if col_name in histograms:
                for key, value in histograms[col_name].items():
                    stats.add(key, value)
            all_stats[col_name] = stats
        return all_stats

    @abc.abstractmethod
    def _get_histograms_for_columns(self, dq_data_columns: Dict[str, DqDataColumn]) \
            -> Dict[str, Dict[str, int]]:
        pass

    def get_sample_stats(self, sample_data: pd.DataFrame,
                         data_column_collection: DqDataColumnCollection) -> SampleStatistics:
        """Calculates statistics for calculation input sample"""
        if sample_data is None:
            raise KnownException("Calculation process cancelled because table is empty")
        dataframe = DataFrame()
        dataframe.data_frame = sample_data
        new_col_metadata_list = self.calc_params.column_dq_metadata_list
        filtered_metadata_col = [col for col in new_col_metadata_list if col.inclusion_flag]
        return self.__compute_stats(dataframe, filtered_metadata_col, data_column_collection)

    def __compute_stats(self, data: DataFrame, col_metadata_list: List[DqColumnMetadata],
                        data_column_collection: DqDataColumnCollection) -> SampleStatistics:
        data_columns = {col.column_name: col for col in data_column_collection}
        categorical_cols = []
        numerical_cols = []
        for col in col_metadata_list:
            if col.column_name not in data.get_column_names():
                raise KnownException("Column not in dataframe")
            col_native_type = data_columns[col.column_name].column_native_type
            if col_native_type == ColumnNativeType.Numeric:
                numerical_cols.append(col)
            elif col_native_type in self.calc_params.nominal_column_types:
                categorical_cols.append(col)
        missing_values = {col.column_name: col.default_values for col in categorical_cols}

        stats = DqStatisticsDomainService.compute_categorical_statistics(data, missing_values)
        sample_stats = SampleStatistics()
        sample_stats.nominal_statistics = {col_name: stat for col_name, stat in stats.items()
                                           if stat.cardinality <= self.calc_params.max_nominal_cardinality_count}
        default_values_by_col = {col.column_name: self.__get_default_values(col.default_values)
                                 for col in numerical_cols}
        sample_stats.numerical_statistics = \
            DqStatisticsDomainService.compute_numerical_statistics(data, default_values_by_col,
                                                                   self.calc_params.outlier_parameter)
        return sample_stats

    @staticmethod
    def __get_default_values(default_values: List[str]) -> List[float]:
        float_vals = []
        nan_exists = False
        for val in default_values:
            try:
                float_val = float(val)
            except ValueError:
                continue
            if math.isnan(float_val):
                nan_exists = True
            float_vals.append(float_val)
        if not nan_exists:
            float_vals.append(float("nan"))
        return float_vals

    def update_calc_params(self, col_collection: DqDataColumnCollection) -> List[DqColumnMetadata]:
        """Updates calculation metadata list using column info"""
        return self.__update_column_dq_metadata_list(col_collection)

    def __update_column_dq_metadata_list(self, col_collection: DqDataColumnCollection) -> List[DqColumnMetadata]:
        """Updates calculation metadata list using column info"""
        calc_params = self.calc_params
        col_meta_dict: Dict[str, DqColumnMetadata] = {col.column_name: col for col in
                                                      calc_params.column_dq_metadata_list}
        eligible_types = [ColumnNativeType.Numeric] + calc_params.nominal_column_types
        for col in col_collection:
            if col.column_native_type in eligible_types:
                if col.column_name in col_meta_dict:
                    col_meta = col_meta_dict[col.column_name]
                    col_meta.inclusion_flag = True if col_meta.inclusion_flag is None else col_meta.inclusion_flag
                    col_meta.default_values = [] if list_helper.is_null_or_empty(col_meta.default_values) \
                        else col_meta.default_values
                else:
                    new_meta = DqColumnMetadata()
                    new_meta.column_name = col.column_name
                    new_meta.inclusion_flag = True
                    new_meta.default_values = []
                    col_meta_dict[col.column_name] = new_meta
            else:
                if col.column_name in col_meta_dict:
                    col_meta_dict.pop(col.column_name)
        metadata_list = list(col_meta_dict.values())
        self.calc_params.column_dq_metadata_list = metadata_list
        return metadata_list
