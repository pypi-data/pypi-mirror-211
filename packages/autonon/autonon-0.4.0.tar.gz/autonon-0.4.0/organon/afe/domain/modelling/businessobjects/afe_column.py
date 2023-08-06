"""
This module includes AfeColumn class.
"""
from typing import List, Dict, Any

import numpy as np

from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.fl.core.helpers import string_helper


class AfeColumn:
    """
    Keeps metadata for a generated Afe column.
    Columns will be used when building modelling and scoring data.
    """

    def __init__(self):
        self._column_name: str = None
        self.date_column: AfeDateColumn = None
        self.dimension_name: str = None
        self.quantity_name: str = None
        self.operator: AfeOperator = None
        self.group_id: int = None
        self.set: List[np.short] = None
        self.in_out: bool = None
        self.date_resolution: DateResolution = None
        self.offset: int = None
        self.time_window: int = None
        self.source: str = None

    @property
    def column_name(self) -> str:
        """Return value of private attribute '__column_name'"""
        return self._column_name

    def set_column_name(self):
        """
        Sets column name using other attributes
        :return:
        """
        if self.date_column is None:
            date_column_name = ""
        else:
            date_column_name = self.date_column.column_name

        self._column_name = AfeColumn.build_column_name(self.group_id, self.dimension_name, self.quantity_name,
                                                        self.operator.name,
                                                        date_column_name,
                                                        self.time_window)

    def get_group_name(self) -> str:
        """
        Returns group name.
        :return: str
        """
        return f"{self.dimension_name}_{self.quantity_name}_{self.operator.name}_{self.time_window}"

    def get_dimension_set(self, _map: Dict[int, str]) -> str:
        """
        Returns dimension set.
        :type _map: Dict[int, str]
        :return: str
        """
        if len(_map) == 0:
            return ""
        ret_str = ""
        if not self.in_out:
            ret_str += "~"
        for i, elem in enumerate(self.set):
            if _map[elem] is not None:
                token = string_helper.filter_non_alpha_numeric(
                    _map[elem])  # pylint: disable=unsubscriptable-object
                ret_str += token
            else:
                ret_str += "None"

            if i < len(self.set) - 1:
                ret_str += "&"

        return ret_str

    @staticmethod
    def build_column_name(val, dimension_name: str, quantity_name: str, afe_operator_name: str,
                          trx_date_column: str,
                          time_window) -> str:
        """
        Builds and returns column name
        :return: str
        """

        ret_str = f"{dimension_name}_{quantity_name}_{val}_{afe_operator_name}_{trx_date_column}_{time_window}"

        return ret_str

    @staticmethod
    def build_column_name_for_list_value(val: List[Any], dimension_name, quantity_name, afe_op,
                                         time_window) -> str:
        """
        Builds and returns column name
        :return: str
        """

        val_str = "_".join([str(i) for i in val])

        ret_str = f"{dimension_name}_{quantity_name}_{val_str}_{afe_op.name}"

        if time_window is not None:
            ret_str += "_" + str(time_window)

        return ret_str

    def build_column_name_with_map(self, _map: Dict[np.int16, str]) -> str:
        """
        Builds and returns column name using _map
        :param _map:
        :type _map: Dict[int, str]
        :return: column name
        """
        dimension_set = self.get_dimension_set(_map)
        dimension_set_empty = len(dimension_set) == 0

        if dimension_set_empty:
            return f"{self.dimension_name}__{self.quantity_name}__{self.operator.name}__{self.time_window}"
        return f"{self.dimension_name}__{dimension_set}__{self.quantity_name}" \
               f"__{self.operator.name}__{self.time_window}"
