"""Includes SamplingPreprocessingService class"""
from typing import List

import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.common.helpers.df_ops_helper import get_bins


class SamplingPreprocessingService:
    """Service to prepare data before sampling"""

    @classmethod
    def discretize(cls, data: pd.DataFrame, columns: List[str], num_bins: int = 10):
        """Converts high cardinality numeric columns to categorical columns with given number of categories(bins)"""
        numeric_columns = [col for col in columns if get_column_native_type(data, col) == ColumnNativeType.Numeric]
        continuous_cols = cls._get_continuous_column_names(data, numeric_columns)
        for col in continuous_cols:
            data[col] = get_bins(data[col], num_bins)
        return data

    @classmethod
    def _get_continuous_column_names(cls, data: pd.DataFrame, columns: List[str]) -> List[str]:
        data_length = len(data)
        upper_limit = data_length * 0.1
        continuous_cols = [col for col in columns if data[col].nunique() > upper_limit]
        return continuous_cols
