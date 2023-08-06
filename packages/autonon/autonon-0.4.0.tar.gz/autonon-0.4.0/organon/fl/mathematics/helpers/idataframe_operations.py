"""This module includes IDataFrameOperations abstract class."""
import abc
from typing import Dict, Any, List

from organon.fl.core.businessobjects.idataframe import IDataFrame


class IDataFrameOperations(metaclass=abc.ABCMeta):
    """Abstract class for Dataframe Operations."""

    @staticmethod
    @abc.abstractmethod
    def join(df1: IDataFrame, df2: IDataFrame):
        """:returns pandas join function equivalent"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_column_stability(df_obj: IDataFrame):
        """:returns boolean df depends on whether a column is stable or not"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_column_distinct_counts(df_obj: IDataFrame, col_names: List[str] = None) -> Dict[str, int]:
        """:returns number of unique values per column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_min_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        """Returns min value in given column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_max_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        """Returns max value in given column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_mean_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        """Returns mean value in given column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_trimmed_mean_value(df_obj: IDataFrame, col_name: str, lower_bound: float, upper_bound: float) -> float:
        """Returns trimmed mean value in given column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_variance_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        """Returns variance in given column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_sum_value(df_obj: IDataFrame, col_name: str, skipna=True) -> float:
        """Returns sum of values in given column"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_percentile_values(df_obj: IDataFrame, col_name: str, percentiles: List[float]) -> Dict[float, float]:
        """Returns percentile values for given percentiles"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_frequencies(df_obj: IDataFrame, col_name: str, values: list = None) -> Dict[Any, int]:
        """Returns number of occurrences of given values in the given column"""

    @staticmethod
    @abc.abstractmethod
    def get_col_df_without_values(df_obj: IDataFrame, col_name: str, values: list) -> IDataFrame:
        """Returns the given column in a new DataFrame by eliminating given values"""

    @staticmethod
    @abc.abstractmethod
    def get_size(df_obj: IDataFrame):
        """Returns number of rows in dataframe"""

    @staticmethod
    @abc.abstractmethod
    def get_col_values(df_obj: IDataFrame, col_name: str) -> list:
        """Returns column values as list"""
