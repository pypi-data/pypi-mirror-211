"""todo"""
from typing import List

from organon.fl.core.enums.column_native_type import ColumnNativeType


class DqDataColumn:
    """todo"""

    def __init__(self):
        self.column_name: str = None
        self.column_description: str = None
        self.default_values: List[str] = None
        self.column_native_type: ColumnNativeType = None
        self.default_values_numeric: List[float] = None
        self.default_values_nominal: List[str] = None
        self.inclusion_flag: bool = None

    # def __initialize(self):
    #     self.column_name = ""
    #     self.column_description = ""
    #     self.data_type = object
    #     self.column_native_type = ColumnNativeType.Other
    #     self.default_values = []
