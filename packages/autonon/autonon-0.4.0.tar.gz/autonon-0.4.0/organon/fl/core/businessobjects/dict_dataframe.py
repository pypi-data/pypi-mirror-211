"""Includes DictDataFrame class."""
from typing import List, Any, Union, Dict

import numpy as np
import pandas as pd

from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.core.helpers import string_helper, list_helper


class DictDataFrame(IDataFrame):
    """Dictionary based custom DataFrame implementing IDataFrame abstract class."""

    def __init__(self, row_count: int = None):
        super().__init__(row_count=row_count)
        self.data_frame: Dict[str, np.array] = {}
        self.__columns_marked_for_gc = []

    def set_value(self, value, column_name: str, row_index: int):
        self.data_frame[column_name][row_index] = value

    def contains_column(self, column_name: str) -> bool:
        return column_name in self.data_frame

    def try_add(self, column_name: str, data: List[Any], mark_for_garbage_collection: bool = False) -> bool:
        cond1 = string_helper.is_null_or_empty(column_name) or column_name in self.data_frame
        if cond1:
            raise ValueError("Column name is inadmissible")
        cond2 = list_helper.is_null_or_empty(data) or len(data) != self.row_count
        if cond2:
            raise ValueError("Data length should be equal to frame-row-count")
        if data is not None and len(data) > 0 and isinstance(data[0], str):
            self.data_frame[column_name] = np.array(data)
        else:
            self.data_frame[column_name] = np.array(data, dtype=np.float32)
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
            del self.data_frame[col]

    def get_value(self, column_name: str, row_index: int = None):
        column = self.data_frame[column_name]
        if row_index is not None:
            return column[row_index]
        return column

    def collect_garbage_columns(self):
        self.remove(self.__columns_marked_for_gc)
        self.__columns_marked_for_gc.clear()

    def get_column_names(self) -> List[str]:
        return list(self.data_frame.keys())

    def get_subset_as_pandas_df(self, indices: List[Any] = None, columns: List[str] = None):
        subset = {}
        if indices is None and columns is None:
            raise ValueError("Both indices and columns are None")

        if indices is None:
            subset = {col: self.data_frame[col] for col in columns}
        elif columns is None:
            for col, values in self.data_frame.items():
                subset[col] = [values[i] for i in indices]
        else:
            for col in columns:
                val = self.data_frame[col]
                subset[col] = [val[i] for i in indices]
        return pd.DataFrame(subset)

    def copy_as_pandas_df(self):
        return pd.DataFrame(self.data_frame)
