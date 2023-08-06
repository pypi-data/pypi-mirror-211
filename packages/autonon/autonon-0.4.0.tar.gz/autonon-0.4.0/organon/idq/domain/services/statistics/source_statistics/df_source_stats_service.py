"""todo"""

from typing import Dict, List

import pandas as pd

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.core.helpers.string_helper import to_upper_eng
from organon.fl.mathematics.helpers.pandas_dataframe_operations import PandasDataFrameOperations
from organon.idq.dataaccess.helpers.record_source_filter_helper import RecordSourceFilterHelper
from organon.idq.domain.businessobjects.data_column.dq_df_data_column import DqDfDataColumn
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.businessobjects.dq_data_source import DqDataSource
from organon.idq.domain.services.statistics.source_statistics.dq_source_stats_base_service import \
    DqSourceStatsBaseService
from organon.idq.domain.settings.calculation.dq_df_calculation_parameters import DqDfCalculationParameters
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata


class DfSourceStatsService(DqSourceStatsBaseService[DqDfCalculationParameters]):
    """Service for generating statistics for a dq dataframe source"""

    def __init__(self, calc_params: DqDfCalculationParameters):
        super().__init__(calc_params)
        self.record_source = RecordSourceFilterHelper.get_filtered_dataframe(
            self.calc_params.input_source_settings.source.locator,
            self.calc_params.input_source_settings)

    def _get_column_cardinalities_from_population(self, column_names: List[str]) -> Dict[str, int]:
        frame = DataFrame()
        frame.data_frame = self.record_source
        return PandasDataFrameOperations.get_column_distinct_counts(frame, column_names)

    def _get_histograms_for_columns(self, dq_data_columns: Dict[str, DqDfDataColumn]) \
            -> Dict[str, Dict[str, int]]:
        frame = DataFrame()
        frame.data_frame = self.record_source
        column_names = list(dq_data_columns.keys())
        all_frequencies = {}
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
            all_frequencies[col] = col_frequencies
        return all_frequencies

    def get_data_column_collection(self, data_source: DqDataSource, columns_dq_metadata: List[DqColumnMetadata]) \
            -> DqDataColumnCollection:
        collection = DqDataColumnCollection()
        dq_metadata_dict: Dict[str, DqColumnMetadata] = \
            {to_upper_eng(col.column_name): col for col in columns_dq_metadata}
        for col in data_source.sampled_data.columns:
            dq_data_col = DqDfDataColumn()
            dq_data_col.column_name = col
            dq_data_col.col_np_dtype = data_source.sampled_data.dtypes[col]
            dq_metadata = dq_metadata_dict.get(to_upper_eng(col), None)
            if dq_metadata is not None:
                dq_data_col.default_values = dq_metadata.default_values
                dq_data_col.inclusion_flag = dq_metadata.inclusion_flag
            dq_data_col.column_native_type = get_column_native_type(data_source.sampled_data, col)
            collection.add(dq_data_col)
        return collection
