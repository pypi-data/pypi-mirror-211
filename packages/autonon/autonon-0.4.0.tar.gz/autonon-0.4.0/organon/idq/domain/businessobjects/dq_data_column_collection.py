"""Includes DqDataColumnCollection class."""
from typing import List, Optional

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.idq.domain.businessobjects.data_column.dq_data_column import DqDataColumn


class DqDataColumnCollection:
    """Collection of DqDataColumn instances."""

    def __init__(self):
        self.column_list: List[DqDataColumn] = []

    def get_columns(self, col_native_type: ColumnNativeType) -> List[DqDataColumn]:
        """Returns columns with given native type"""
        return [col for col in self.column_list if col.column_native_type == col_native_type]

    def get_column(self, col_name: str) -> Optional[DqDataColumn]:
        """Returns columns with given name. Returns None if not found."""
        for col in self.column_list:
            if col.column_name == col_name:
                return col
        return None

    def get_eligible_columns(self) -> List[DqDataColumn]:
        """Returns eligible columns"""
        return [col for col in self.column_list if col.column_native_type != ColumnNativeType.Other]

    def get_partition_columns(self) -> List[DqDataColumn]:
        """Returns list of columns which are partitionable"""
        return [col for col in self.column_list if col.column_native_type != ColumnNativeType.Other]

    def remove(self, col_name: str):
        """removes column by name"""
        col_to_remove = None
        for col in self.column_list:
            if col.column_name == col_name:
                col_to_remove = col
        if col_to_remove is not None:
            self.column_list.remove(col_to_remove)

    def add(self, item: DqDataColumn):
        """adds item to collection"""
        self.column_list.append(item)

    def __iter__(self):
        return iter(self.column_list)
