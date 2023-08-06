"""
This module keeps Histogram16 class.
"""
from typing import TypeVar, Dict, List, Generic
import numpy as np
from organon.fl.core.helpers.dict_helper import add_if_key_not_exist
from organon.fl.core.collections.pair import Pair
T1 = TypeVar('T1')


class Histogram16(Generic[T1]):
    """
    This class keeps the features of histogram and the functions used in histograms such as build indices.
    """
    def __init__(self):
        self.__frequencies: Dict[T1, np.int64] = {}
        self.__index: Dict[T1, np.int16] = {}
        self.__reverse_index: Dict[np.int16, T1] = {}
        self.__compressed_index: Dict[T1, np.int16] = {}
        self.__compressed_reverse_index: Dict[np.int16, List[T1]] = {}
        self.__original_2_compressed: Dict[np.int16, np.int16] = {}
        self.__bulk_set_index: np.int16 = np.int16(-1)
        self.__bulk_set: List[T1] = []

    @property
    def frequencies(self) -> Dict[T1, np.int64]:
        """
        Returns the frequencies dictionary.
        :return: frequencies dictionary
        """
        return self.__frequencies

    @property
    def index(self) -> Dict[T1, np.int16]:
        """
        Returns the index dictionary.
        :return: index dictionary
        """
        return self.__index

    @property
    def reverse_index(self) -> Dict[np.int16, T1]:
        """
        Returns the reverse_index dictionary.
        :return: reverse_index dictionary
        """
        return self.__reverse_index

    @property
    def compressed_index(self) -> Dict[T1, np.int16]:
        """
        Returns the compressed_index dictionary.
        :return: compressed_index dictionary
        """
        return self.__compressed_index

    @property
    def compressed_reverse_index(self) -> Dict[np.int16, List[T1]]:
        """
        Returns the compressed_reverse_index dictionary.
        :return: compressed_reverse_index dictionary
        """
        return self.__compressed_reverse_index

    @property
    def original_to_compressed(self) -> Dict[np.int16, np.int16]:
        """
        Returns the original_2_compressed dictionary.
        :return: original_2_compressed dictionary
        """
        return self.__original_2_compressed

    @property
    def bulk_set_index(self) -> np.int16:
        """
        Returns bulk_set_index value.
        :return: bulk_set_index value
        """
        return self.__bulk_set_index

    @property
    def bulk_set(self) -> List[T1]:
        """
        Returns bulk_set_index.
        :return: bulk_set_index
        """
        return self.__bulk_set

    def get_index_value(self, key: T1) -> np.int16:
        """
        Returns the key's value in index dictionary.
        :param key: key of index dictionary
        :return: the key's value in index dictionary
        """
        return self.__index[key]

    def build_indices(self):
        """
        Builds the indices of the histogram
        :return: nothing
        """
        freq_length: int = len(self.__frequencies)
        list1: List[Pair[np.float64, T1]] = [None] * freq_length
        frequency_sum: np.float64 = np.float64(0.0)
        index: int = 0
        for item, value in self.__frequencies.items():
            list1[index] = (Pair(value, item))
            frequency_sum += self.__frequencies[item]
            index += 1
        list1.sort()

        list2: List[Pair[np.float64, T1]] = [None] * freq_length
        index = 0
        for pair in reversed(list1):
            list2[index] = Pair(pair.first / frequency_sum, pair.second)
            index += 1
        for pair in list2:
            percentage: np.float64 = pair.first
            key: T1 = pair.second
            if percentage >= 0.01:
                add_if_key_not_exist(key, self.__index[key], self.__compressed_index)
                add_if_key_not_exist(self.__index[key], [key], self.__compressed_reverse_index)
            else:
                if self.__bulk_set_index not in self.__compressed_reverse_index:
                    self.__compressed_reverse_index[self.__bulk_set_index] = []
                add_if_key_not_exist(key, self.__bulk_set_index, self.__compressed_index)
                self.__compressed_reverse_index[self.__bulk_set_index].append(key)
                self.__bulk_set.append(key)

        keys: List[T1] = list(self.__index.keys())
        for key in keys:
            add_if_key_not_exist(self.__index[key], self.__compressed_index[key],
                                 self.__original_2_compressed)

    def build_indices_with_params(self, compression_ration: float, max_cardinality: int):
        """
        Builds the indices of the histogram according to the compression ratio and max cardinality
        :param compression_ration: measurement of the relative reduction in size of data representation
        produced by a data compression algorithm
        :param max_cardinality: maximum number of entity instances that can participate in a relationship
        :return: nothing
        """
        freq_length: int = len(self.__frequencies)
        list1: List[Pair[np.float64, T1]] = [None] * freq_length
        index: int = 0
        for item, value in self.__frequencies.items():
            list1[index] = Pair(value, item)
            # list1.append(Pair(self.__frequencies[item], item))
            index += 1

        list1.sort()
        list2: List[Pair[np.float64, T1]] = [None] * freq_length
        last_pair: Pair[np.float64, T1] = list1[freq_length-1]
        list2[0] = Pair(last_pair.first, last_pair.second)
        grand_sum: np.float64 = last_pair.first
        if len(list1) > 1:
            index = 1
            reversed_list1 = reversed(list1[:-1])
            for pair in reversed_list1:
                grand_sum += pair.first
                list2[index] = Pair(grand_sum, pair.second)
                index += 1

        # list1.clear()
        list3: List[Pair[np.float64, T1]] = [None] * freq_length
        index = 0
        for pair in list2:
            list3[index] = Pair(pair.first / grand_sum, pair.second)
            index += 1

        # list2.clear()
        found: bool = False
        index: int = 0
        for pair in list3:
            percentage: np.float64 = pair.first
            key: T1 = pair.second
            # mark: np.int16 = np.int16(list3.index(pair))
            # self.index.update({key: mark})
            if percentage <= compression_ration and index < max_cardinality:
                add_if_key_not_exist(key, self.__index[key], self.__compressed_index)
                add_if_key_not_exist(self.__index[key], [key], self.__compressed_reverse_index)
            else:
                if not found:
                    found = True
                    # self.bulk_set_index = mark
                    add_if_key_not_exist(key, self.__index[key], self.__compressed_index)
                    add_if_key_not_exist(self.__index[key], [key], self.__compressed_reverse_index)
                else:
                    if self.__bulk_set_index not in self.__compressed_reverse_index:
                        self.__compressed_reverse_index[self.__bulk_set_index] = []
                    add_if_key_not_exist(key, self.__bulk_set_index, self.__compressed_index)
                    self.__compressed_reverse_index[self.__bulk_set_index].append(key)
                    self.__bulk_set.append(key)
            index += 1
        keys: List[T1] = list(self.__index.keys())
        for key in keys:
            add_if_key_not_exist(self.__index[key], self.__compressed_index[key],
                                 self.__original_2_compressed)

    def add(self, key: T1, frequency: int = None):
        """
        Adds or updates the key's value in the dictionaries.
        :param key: key for index dict, value for reverse index dict
        :param frequency: frequency value
        :return: nothing
        """
        if frequency is None:
            if key in self.__frequencies:
                self.__frequencies[key] += 1
            else:
                self.__frequencies[key] = 1
                index_val: np.int16 = np.int16(len(self.__index))
                add_if_key_not_exist(key, index_val, self.__index)
                add_if_key_not_exist(index_val, key, self.__reverse_index)
        else:
            if key in self.__frequencies:
                self.__frequencies[key] += frequency
            else:
                self.__frequencies[key] = frequency
                index_val: np.int16 = np.int16(len(self.__index))
                add_if_key_not_exist(key, index_val, self.__index)
                add_if_key_not_exist(index_val, key, self.__reverse_index)
