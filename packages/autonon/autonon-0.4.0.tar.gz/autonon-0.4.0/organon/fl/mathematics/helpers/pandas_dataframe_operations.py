""" This module includes PandasDataFrameOperations."""
import math
from typing import Dict, Any, List

import pandas as pd

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.fl.mathematics.helpers.idataframe_operations import IDataFrameOperations


class PandasDataFrameOperations(IDataFrameOperations):
    """Class for Pandas Dataframe Operations."""

    @staticmethod
    def join(df1: DataFrame, df2: DataFrame):
        """:returns pandas join function equivalent"""
        joined_df = DataFrame()
        joined_df.data_frame = df1.data_frame.join(df2.data_frame).fillna(0)
        return joined_df

    @staticmethod
    def get_column_stability(df_obj: DataFrame):
        """:returns boolean df depends on whether a column is stable or not"""
        df_to_numpy = df_obj.data_frame.to_numpy()
        return (df_to_numpy[0] == df_to_numpy).all(0) | df_obj.data_frame.isnull().all()

    @staticmethod
    def get_column_distinct_counts(df_obj: DataFrame, col_names: List[str] = None) -> Dict[str, int]:
        """:returns number of unique values per column"""
        df_to_pandas_df = df_obj.data_frame
        cols = col_names if col_names is not None else df_to_pandas_df.columns
        return {col: df_to_pandas_df[col].nunique(dropna=False) for col in cols}

    @staticmethod
    def get_min_value(df_obj: DataFrame, col_name: str, skipna=True) -> float:
        return df_obj.data_frame[col_name].min(skipna=skipna)

    @staticmethod
    def get_max_value(df_obj: DataFrame, col_name: str, skipna=True) -> float:
        """Returns max value in given column"""
        return df_obj.data_frame[col_name].max(skipna=skipna)

    @staticmethod
    def get_mean_value(df_obj: DataFrame, col_name: str, skipna=True) -> float:
        """Returns mean value in given column"""
        return df_obj.data_frame[col_name].mean(skipna=skipna)

    @staticmethod
    def get_trimmed_mean_value(df_obj: DataFrame, col_name: str, lower_bound: float, upper_bound: float) -> float:
        """Returns trimmed mean value in given column"""
        col = df_obj.data_frame[col_name]
        return col[(col >= lower_bound) & (col <= upper_bound)].mean()

    @staticmethod
    def get_variance_value(df_obj: DataFrame, col_name: str, skipna=True) -> float:
        """Returns variance in given column"""
        variance = df_obj.data_frame[col_name].var(skipna=skipna)
        return variance if not pd.isna(variance) else float("nan")

    @staticmethod
    def get_sum_value(df_obj: DataFrame, col_name: str, skipna=True) -> float:
        """Returns sum of values in given column"""
        return df_obj.data_frame[col_name].sum(skipna=skipna)

    @staticmethod
    def get_percentile_values(df_obj: DataFrame, col_name: str, percentiles: List[float]) -> Dict[float, float]:
        """Returns percentile values for given percentiles"""
        ret = {}
        for val in percentiles:
            ret[val] = df_obj.data_frame[col_name].quantile(val / 100.0, interpolation="lower")
        return ret

    @staticmethod
    def get_frequencies(df_obj: DataFrame, col_name: str, values: list = None) -> Dict[Any, int]:
        ret = {}
        if values is not None:
            for val in values:
                if isinstance(val, float) and math.isnan(val):
                    ret[None] = df_obj.data_frame[col_name].isnull().sum()
                else:
                    ret[val] = (df_obj.data_frame[col_name].values == val).sum()
            return ret
        val_df = df_obj.data_frame[col_name].value_counts(dropna=False).to_dict()
        for key, val in val_df.items():
            new_key = key
            if pd.isna(key):
                new_key = None
                if val == 0:
                    continue
            ret[new_key] = val

        return ret

    @staticmethod
    def get_col_df_without_values(df_obj: DataFrame, col_name: str, values: list) -> DataFrame:
        col_df = df_obj.data_frame[col_name]
        col_filter = ~col_df.isin(values)
        nan_excluded = sum(1 for x in values if isinstance(x, float) and math.isnan(x)) > 0
        if nan_excluded:
            col_filter &= ~col_df.isnull()
        new_df = DataFrame()
        new_df.data_frame = col_df[col_filter].to_frame()
        return new_df

    @staticmethod
    def get_size(df_obj: DataFrame):
        return len(df_obj.data_frame)

    @staticmethod
    def get_col_values(df_obj: DataFrame, col_name: str) -> list:
        return df_obj.data_frame[col_name].tolist()

    @staticmethod
    def get_unique_values_in_column(df_obj: DataFrame, col_name: str) -> List:
        """Returns unique values in the given column of dataframe"""
        return df_obj.data_frame[col_name].unique().tolist()
