"""Includes Dask DataFrame class for future development"""
from typing import List, Union, Any

from organon.fl.core.businessobjects.idataframe import IDataFrame


class DaskDataFrame(IDataFrame):
    """Dask DataFrame based custom DataFrame implementing IDataFrame abstract class."""

    def set_value(self, value, column_name: str, row_index: int):
        raise NotImplementedError()

    def contains_column(self, column_name: str) -> bool:
        raise NotImplementedError()

    def try_add(self, column_name: str, data: List[Any], mark_for_garbage_collection: bool = False):
        raise NotImplementedError()

    def remove(self, column_names: Union[List[str], str]):
        raise NotImplementedError()

    def collect_garbage_columns(self):
        raise NotImplementedError()

    def get_value(self, column_name: str, row_index: int = None):
        raise NotImplementedError()

    def get_column_names(self) -> List[str]:
        raise NotImplementedError()

    def get_subset_as_pandas_df(self, indices: List[Any] = None, columns: List[str] = None):
        raise NotImplementedError()

    def copy_as_pandas_df(self):
        raise NotImplementedError()
