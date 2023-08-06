"""Includes PartitionInfo class."""
from typing import Union, List

from organon.fl.core.helpers import list_helper
from organon.idq.domain.settings.date_value_definition import DateValueDefinition


class PartitionInfo:
    """Dq column partition info."""

    def __init__(self):
        self.column_name: str = None
        self.column_values: Union[List[DateValueDefinition], List[float], List[str]] = None

    def to_str(self):
        """return partition info as str"""
        return f"[{self.column_name}={self.get_col_val_str()}]"

    def get_col_val_str(self) -> str:
        """returns partition info column values as str"""
        column_values = self.column_values
        if list_helper.is_null_or_empty(column_values):
            return ""
        col_val_str_parts = []
        for val in column_values:
            if isinstance(val, DateValueDefinition):
                col_val_str_parts.append(self.__get_col_val_str_for_date_value_partition_definition(val))
            else:
                col_val_str_parts.append(str(val))

        col_val_str = "(" + ",".join(col_val_str_parts) + ")"
        return col_val_str

    @classmethod
    def __get_col_val_str_for_date_value_partition_definition(cls, definition: DateValueDefinition) -> str:
        parts = []
        if definition.year is not None:
            parts.append(f"y={definition.year}")
        if definition.month is not None:
            parts.append(f"m={definition.month}")
        if definition.day is not None:
            parts.append(f"d={definition.day}")
        if definition.hour is not None:
            parts.append(f"h={definition.hour}")
        ret = "{" + ",".join(parts) + "}"
        return ret
