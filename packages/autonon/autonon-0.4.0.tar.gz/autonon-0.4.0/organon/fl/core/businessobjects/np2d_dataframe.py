"""Includes DictDataFrame class."""
from typing import List, Any, Union, Dict

import numpy as np
import pandas as pd

from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.core.helpers import string_helper, list_helper


class Np2dDataFrame(IDataFrame):
    """Dictionary based custom DataFrame implementing IDataFrame abstract class."""

    def __init__(self, row_count: int, max_column_count: int, dtype: type):
        super().__init__(row_count=row_count)
        self.max_column_count = max_column_count
        self.dtype = dtype
        self.data_frame: np.ndarray = np.full((row_count, max_column_count), None, dtype=dtype)
        self.column_name_map: Dict[str, int] = {}
        self.empty_column_indices: List[int] = list(range(max_column_count))
        self.column_name_reverse_map: Dict[int, str] = {}
        self.__columns_marked_for_gc = []

    def set_value(self, value, column_name: str, row_index: int):
        index = self.column_name_map[column_name]
        self.data_frame[row_index][index] = value

    def contains_column(self, column_name: str) -> bool:
        return column_name in self.column_name_map

    def try_add(self, column_name: str, data: List[Any] = None, mark_for_garbage_collection: bool = False) -> bool:
        cond1 = string_helper.is_null_or_empty(column_name) or column_name in self.column_name_map
        if cond1:
            raise ValueError("Column name is inadmissible")
        cond2 = not list_helper.is_null_or_empty(data) and len(data) != self.row_count
        if cond2:
            raise ValueError("Data length should be equal to frame-row-count")
        if len(self.empty_column_indices) == 0:
            raise ValueError("Np2dDataFrame has all columns full.")
        new_index = self.empty_column_indices[0]
        self.column_name_map[column_name] = new_index
        self.column_name_reverse_map[new_index] = column_name
        self.empty_column_indices.remove(new_index)
        if data is not None:
            self.data_frame[:, new_index] = np.array(data)
        if mark_for_garbage_collection:
            self.__columns_marked_for_gc.append(column_name)
        return True

    def remove(self, column_names: Union[List[str], str]):
        columns_to_remove = []
        if isinstance(column_names, list):
            columns_to_remove.extend(column_names)
        else:
            columns_to_remove.append(column_names)
        for col in columns_to_remove:
            val = self.column_name_map.pop(col, None)
            if val is not None:
                self.data_frame[:, val] = None
                self.empty_column_indices.append(val)
                self.column_name_reverse_map.pop(val)

    def get_value(self, column_name: str, row_index: int = None):
        index = self.column_name_map[column_name]
        if row_index is not None:
            return self.data_frame[row_index, index]
        return self.data_frame[:, index]

    def collect_garbage_columns(self):
        self.remove(self.__columns_marked_for_gc)
        self.__columns_marked_for_gc.clear()

    def get_column_names(self) -> List[str]:
        return list(self.column_name_map.keys())

    def get_subset_as_pandas_df(self, indices: List[Any] = None, columns: List[str] = None):

        if indices is None and columns is None:
            raise ValueError("Both indices and columns are None")

        if indices is None:
            subset = self.data_frame[:, [self.column_name_map[col] for col in columns]]
        elif columns is None:
            columns = list(self.column_name_map.keys())
            subset = self.data_frame[indices, [self.column_name_map[col] for col in columns]]
        else:
            subset = self.data_frame[indices, [self.column_name_map[col] for col in columns]]
        return pd.DataFrame(subset, columns=columns)

    def copy_as_pandas_df(self):
        column_indices_sorted = sorted(self.column_name_reverse_map.keys())
        columns = []
        for i in column_indices_sorted:
            columns.append(self.column_name_reverse_map[i])
        new_arr = self.data_frame[:, column_indices_sorted]
        return pd.DataFrame(new_arr, columns=columns)

    def rename_columns(self, new_names_dict: Dict[str, str]):
        """
        Renames columns in dataframe
        :param new_names_dict: dictionary mapping old column names to their new names
        """
        new_column_name_map = {}
        new_column_name_reverse_map = {}
        for old_name, new_name in new_names_dict.items():
            col_index = self.column_name_map[old_name]
            new_column_name_map[new_name] = col_index
            new_column_name_reverse_map[col_index] = new_name

        self.column_name_map = new_column_name_map
        self.column_name_reverse_map = new_column_name_reverse_map

    def get_column_name_by_index(self, col_index: int):
        """Returns column name corresponding to given index"""
        return self.column_name_reverse_map[col_index]
