""" This module includes DaskDataFrameOperations class."""
from typing import List, Dict, Any

from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.mathematics.helpers.idataframe_operations import IDataFrameOperations


class DaskDataFrameOperations(IDataFrameOperations):
    """Class for Dask Dataframe Operations."""

    @staticmethod
    def join(df1: IDataFrame, df2: IDataFrame):
        raise NotImplementedError()

    @staticmethod
    def get_column_stability(df_obj: IDataFrame):
        raise NotImplementedError()

    @staticmethod
    def get_column_distinct_counts(df_obj: IDataFrame, col_names: List[str] = None) -> Dict[str, int]:
        raise NotImplementedError()

    @staticmethod
    def get_min_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_max_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_mean_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_trimmed_mean_value(df_obj: IDataFrame, col_name: str, lower_bound: float, upper_bound: float) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_variance_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_sum_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_percentile_values(df_obj: IDataFrame, col_name: str, percentiles: List[float]) -> Dict[float, float]:
        raise NotImplementedError()

    @staticmethod
    def get_frequencies(df_obj: IDataFrame, col_name: str, values: list = None) -> Dict[Any, int]:
        raise NotImplementedError()

    @staticmethod
    def get_col_df_without_values(df_obj: IDataFrame, col_name: str, values: list) -> IDataFrame:
        raise NotImplementedError()

    @staticmethod
    def get_size(df_obj: IDataFrame):
        raise NotImplementedError()

    @staticmethod
    def get_col_values(df_obj: IDataFrame, col_name: str) -> list:
        raise NotImplementedError()
