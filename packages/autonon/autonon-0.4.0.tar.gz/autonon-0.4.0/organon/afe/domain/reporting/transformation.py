"""
This module includes Transforamtion class.
"""
import locale
from typing import List, Dict
from sortedcontainers import SortedDict

from organon.fl.core.helpers import list_helper


class Transformation:
    """AFE model output transformation"""
    def __init__(self, default_input_list: List[float], default_output: float, map_: SortedDict):
        self.__default_input_list: List[float] = default_input_list
        self.__default_output: float = default_output
        self.__map: SortedDict = map_
        self.__default_input_list.sort()

    @property
    def default_input_list(self):
        """Returns value of private attribute __default_input_list"""
        return self.__default_input_list

    @property
    def default_output(self):
        """Returns value of private attribute __default_output"""
        return self.__default_output

    @property
    def map_(self):
        """Returns value of private attribute __map"""
        return self.__map

    def transform(self, value_to_map: float) -> float:
        """
        Finds corresponding value according to transformation map
        :param value_to_map: map
        :return: Mapped value
        """
        if list_helper.binary_search(self.__default_input_list, value_to_map) != -1:
            return self.__default_output

        for key in self.__map:
            if value_to_map <= key:
                return self.__map[key]
        raise NotImplementedError

    def transform_all(self, input_: List[float]):
        """Transforms all values in list(in place)."""
        for i, val in enumerate(input_):
            input_[i] = self.transform(val)

    def tabulate_as_text(self) -> Dict[str, str]:
        """Converts mappings to a dictionary where keys are ranges of mappings and values are transform values"""
        result: Dict[str, str] = {}
        rounded_default_output = locale.str(round(self.__default_output, 6))
        for _input in self.__default_input_list:
            rounded_value = locale.str(round(_input, 6))
            result[rounded_value] = rounded_default_output
        if self.__map is None or len(self.__map) == 0:
            return result

        keys = list(self.__map.keys())
        values = list(self.__map.values())

        for i, key in enumerate(keys):
            down_string = "-Infty" if i == 0 else locale.str(round(keys[i - 1], 6))
            up_string = "+Infty" if i == len(keys)-1 else locale.str(round(key, 6))
            interval = f"[{down_string}, {up_string})"
            result[interval] = locale.str(round(values[i], 6))

        return result
