"""This module includes DictDataFrameOperations class"""
from typing import List, Dict, Any

from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.mathematics.helpers.idataframe_operations import IDataFrameOperations


class DictDataFrameOperations(IDataFrameOperations):
    """Class for Dictionary Dataframe Operations."""

    @staticmethod
    def get_min_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        pass

    @staticmethod
    def get_max_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        pass

    @staticmethod
    def get_mean_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        pass

    @staticmethod
    def get_trimmed_mean_value(df_obj: IDataFrame, col_name: str, lower_bound: float, upper_bound: float) -> float:
        pass

    @staticmethod
    def get_variance_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        pass

    @staticmethod
    def get_sum_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        pass

    @staticmethod
    def get_percentile_values(df_obj: IDataFrame, col_name: str, percentiles: List[float]) -> Dict[float, float]:
        pass

    @staticmethod
    def get_frequencies(df_obj: IDataFrame, col_name: str, values: list = None) -> Dict[Any, int]:
        pass

    @staticmethod
    def get_col_df_without_values(df_obj: IDataFrame, col_name: str, values: list) -> IDataFrame:
        pass

    @staticmethod
    def get_size(df_obj: IDataFrame):
        pass

    @staticmethod
    def get_col_values(df_obj: IDataFrame, col_name: str) -> list:
        pass

    @staticmethod
    def get_column_stability(df_obj: IDataFrame):
        """:returns boolean df depends on whether a column is stable or not"""
        raise NotImplementedError

    @staticmethod
    def join(df1: DictDataFrame, df2: DictDataFrame):
        """:returns pandas join function equivalent for dict"""
        raise NotImplementedError

    @staticmethod
    def get_column_distinct_counts(df_obj: DictDataFrame, col_names: List[str] = None):
        """:returns number of unique values per column"""
        raise NotImplementedError
