"""todo"""

from typing import Dict, List, Set

import pandas as pd

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.extensions.string_extensions import to_upper_eng
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.mathematics.helpers.pandas_dataframe_operations import PandasDataFrameOperations
from organon.idq.dataaccess.helpers.record_source_filter_helper import RecordSourceFilterHelper
from organon.idq.domain.businessobjects.data_column.dq_file_data_column import DqFileDataColumn
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.businessobjects.dq_data_source import DqDataSource
from organon.idq.domain.services.statistics.source_statistics.dq_source_stats_base_service import \
    DqSourceStatsBaseService
from organon.idq.domain.settings.calculation.dq_file_calculation_parameters import DqFileCalculationParameters
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata


class FileSourceStatsService(DqSourceStatsBaseService[DqFileCalculationParameters]):
    """Service for generating statistics for a dq file source"""

    def __init__(self, calc_params: DqFileCalculationParameters):
        super().__init__(calc_params)
        self.record_source = calc_params.input_source_settings.source.locator

    def _get_column_cardinalities_from_population(self, column_names: List[str]) -> Dict[str, int]:
        distinct_values_by_col: Dict[str, Set] = {col: set() for col in column_names}
        for data_frame in RecordSourceFilterHelper.read_csv_with_chunks(self.calc_params.input_source_settings):
            frame = DataFrame()
            frame.data_frame = data_frame
            for col in column_names:
                distinct_values_by_col[col].update(
                    PandasDataFrameOperations.get_unique_values_in_column(frame, col))
        return {col: len(distinct_values) for col, distinct_values in distinct_values_by_col.items()}

    def _get_histograms_for_columns(self, dq_data_columns: Dict[str, DqFileDataColumn]) \
            -> Dict[str, Dict[str, int]]:
        column_names = list(dq_data_columns.keys())
        all_frequencies: Dict[str, Dict[str, int]] = {col: {} for col in column_names}

        for data_frame in RecordSourceFilterHelper.read_csv_with_chunks(self.calc_params.input_source_settings):
            frame = DataFrame()
            frame.data_frame = data_frame
            for col in column_names:
                col_native_type = dq_data_columns[col].column_native_type
                col_frequencies = PandasDataFrameOperations.get_frequencies(frame, col)
                if col_native_type == ColumnNativeType.Numeric:
                    col_frequencies = {str(key): val for key, val in col_frequencies.items()}
                elif col_native_type == ColumnNativeType.Date:
                    new_dict = {}
                    for val, count in col_frequencies.items():
                        date_val: pd.Timestamp = val
                        new_dict[date_val.strftime("%Y%m%d")] = count
                    col_frequencies = new_dict
                current_frequencies_for_column = all_frequencies[col]
                for value, count in col_frequencies.items():
                    current_count = current_frequencies_for_column.get(value, None)
                    if current_count is not None:
                        current_frequencies_for_column[value] += count
                    else:
                        current_frequencies_for_column[value] = count

        return all_frequencies

    def get_data_column_collection(self, data_source: DqDataSource, columns_dq_metadata: List[DqColumnMetadata]) \
            -> DqDataColumnCollection:
        collection = DqDataColumnCollection()
        dq_metadata_dict: Dict[str, DqColumnMetadata] = \
            {to_upper_eng(col.column_name): col for col in columns_dq_metadata}
        for col in data_source.sampled_data.columns:
            dq_data_col = DqFileDataColumn()
            dq_data_col.column_name = col
            dq_data_col.col_np_dtype = data_source.sampled_data.dtypes[col]
            dq_metadata = dq_metadata_dict.get(to_upper_eng(col), None)
            if dq_metadata is not None:
                dq_data_col.default_values = dq_metadata.default_values
                dq_data_col.inclusion_flag = dq_metadata.inclusion_flag
            dq_data_col.column_native_type = get_column_native_type(data_source.sampled_data, col)
            collection.add(dq_data_col)
        return collection
