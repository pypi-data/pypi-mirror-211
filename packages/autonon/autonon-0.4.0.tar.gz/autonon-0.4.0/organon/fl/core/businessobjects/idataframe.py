"""Includes abstract class(IDataFrame) for custom DataFrame classes."""
import abc
from typing import List, Any, Union


class IDataFrame(metaclass=abc.ABCMeta):
    """Abstract base class for custom DataFrame classes."""

    def __init__(self, row_count: int = None):
        self.data_frame = None
        self.row_count = row_count

    @abc.abstractmethod
    def set_value(self, value, column_name: str, row_index: int):
        """Sets value of a cell in the given column and row"""
        raise NotImplementedError

    @abc.abstractmethod
    def contains_column(self, column_name: str) -> bool:
        """Checks if column is in dataframe"""
        raise NotImplementedError

    @abc.abstractmethod
    def try_add(self, column_name: str, data: List[Any], mark_for_garbage_collection: bool = False):
        """Sets given data as value of given column"""
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, column_names: Union[List[str], str]):
        """Removes given columns from dataframe"""
        raise NotImplementedError

    @abc.abstractmethod
    def collect_garbage_columns(self):
        """Removes columns marked for garbage collection from dataframe"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_value(self, column_name: str, row_index: int = None):
        """Returns all values in column if row_index is None. Else, return value at given column and row."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_column_names(self) -> List[str]:
        """Returns all column names"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_subset_as_pandas_df(self, indices: List[Any] = None, columns: List[str] = None):
        """Returns a subset of dataframe which only includes given columns and given indices."""
        raise NotImplementedError

    @abc.abstractmethod
    def copy_as_pandas_df(self):
        """Returns a copy of dataframe as pandas dataframe"""
        raise NotImplementedError
