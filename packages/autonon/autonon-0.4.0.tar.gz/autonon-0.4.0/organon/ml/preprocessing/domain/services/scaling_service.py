"""Includes ScalingService class"""
from typing import List

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.preprocessing.settings.enums.scaler_type import ScalerType
from organon.ml.preprocessing.settings.objects.scaling_settings import ScalingSettings


class ScalingService:
    """Scales numeric data according to scaling strategy"""

    def __init__(self, settings: ScalingSettings):
        self._settings = settings
        self._scaler_per_col: dict = None
        self._numerical_cols: List[str] = None

    def columns_(self):
        """Returns fitted columns to scale"""
        return self._numerical_cols

    def fit(self, data: pd.DataFrame):
        """Fits scaler"""
        self._scaler_per_col = {}
        self._numerical_cols = [col for col in data.columns if
                                get_column_native_type(data, col) == ColumnNativeType.Numeric]
        for col in self._numerical_cols:
            scaler = self._get_scaler(self._settings.strategy)
            scaler.fit(data[col].values.reshape(-1, 1))
            self._scaler_per_col[col] = scaler
        return self

    def transform(self, data: pd.DataFrame, inplace: bool = False):
        """Transform data"""
        if self._scaler_per_col is None:
            raise ValueError("Scaler not fitted yet")
        if not inplace:
            trans_data = data.copy()
        else:
            trans_data = data
        different_columns = [col for col in trans_data if
                             (get_column_native_type(trans_data, col) == ColumnNativeType.Numeric and
                              col not in self._numerical_cols)]
        if different_columns:
            raise ValueError(f"These numerical columns are not found in the train data or "
                             f"their types were not numerical: {', '.join(different_columns)}.")
        for col, scaler in self._scaler_per_col.items():
            trans_data[col] = scaler.transform(trans_data[col].values.reshape(-1, 1))
        return trans_data

    @staticmethod
    def _get_scaler(strategy: ScalerType):
        """returns appropriate scaler according to scaling strategy"""
        if strategy is ScalerType.MINMAX:
            return MinMaxScaler()
        return StandardScaler()
