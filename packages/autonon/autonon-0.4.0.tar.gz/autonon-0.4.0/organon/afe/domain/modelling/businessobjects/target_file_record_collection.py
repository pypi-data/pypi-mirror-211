"""
This module includes TargetFileRecordCollection class.
"""
from random import Random
from typing import List

import numpy as np

from organon.afe.domain.modelling.businessobjects.target_file_record import TargetFileRecord


class TargetFileRecordCollection:
    """
    Collection of target file records
    """

    def __init__(self, max_record_count: int):
        super().__init__()
        self.max_record_count: int = max_record_count
        self.__sampled: bool = None
        self.__last_filled_index: int = None
        self.__indices: List[int] = None
        self.__entities: np.array = np.full(max_record_count, None, dtype=np.chararray)
        self.__event_dates: np.array = np.full(max_record_count, -1, dtype=np.int64)
        self.__target_binary_values: np.array = np.full(max_record_count, -1, dtype=np.int8)
        self.__target_scalar_values: np.array = np.full(max_record_count, None, dtype=np.float64)
        self.__target_multi_class_values: np.array = np.full(max_record_count, None, dtype=np.object_)

    @property
    def actual_record_count(self) -> int:
        """Number of rows that was filled with data.(Ignoring rows with dummy data)"""
        if self.__last_filled_index is None:
            return 0
        return self.__last_filled_index + 1

    @property
    def sampled(self) -> bool:
        """Returns value of private attribute '__sampled'"""
        return self.__sampled

    @property
    def indices(self) -> List[int]:
        """Returns value of private attribute '__indices'"""
        return self.__indices

    @property
    def entities(self) -> np.ndarray:
        """Returns value of private attribute '__entities'"""
        return self.__entities

    @property
    def event_dates(self) -> np.ndarray:
        """Returns value of private attribute '__event_dates'"""
        return self.__event_dates

    @property
    def target_binary_values(self) -> np.ndarray:
        """Returns value of private attribute '__target_binary_values'"""
        return self.__target_binary_values

    @property
    def target_scalar_values(self) -> np.ndarray:
        """Returns value of private attribute '__target_scalar_values'"""
        return self.__target_scalar_values

    @property
    def target_multi_class_values(self) -> np.ndarray:
        """Returns value of private attribute '__target_scalar_values'"""
        return self.__target_multi_class_values

    @property
    def sampled_count(self) -> int:
        """Returns sampled_count"""
        return len(self.__indices) if self.sampled else self.actual_record_count

    def __get_unique_entities(self) -> List[str]:
        """
        Returns list of unique entity IDs in collection
        :return: List[str]
        """
        _list = []
        for i in range(self.actual_record_count):
            _list.append(self.__entities[i])
        return list(set(_list))

    def get_sampled_unique_entities(self, random_generator: Random, max_entities: int) -> List[str]:
        """
        Returns a list of sampled unique entity IDs
        :param random_generator: Random number generator
        :type random_generator: Random
        :param max_entities:
        :type max_entities: int
        :return: List[str]
        """
        if self.actual_record_count <= max_entities:
            self.__sampled = False
            self.__indices = None
            return self.__get_unique_entities()

        self.__sampled = True
        _list = []
        for i in range(self.actual_record_count):
            _list.append((random_generator.random(), i))
        _list.sort()
        self.__indices = []
        samples = []
        for i in range(max_entities):
            pair = _list[i]
            index = pair[1]
            self.__indices.append(index)
            samples.append(self.entities[index])
        return list(set(samples))

    def append(self, record: TargetFileRecord):
        """Adds given record to record collection"""
        if self.__last_filled_index is None:
            self.__last_filled_index = -1
        self.__last_filled_index += 1
        index = self.__last_filled_index
        self.__entities[index] = record.entity_id
        self.__event_dates[index] = record.event_date
        self.__target_binary_values[index] = record.target_binary.value
        self.__target_scalar_values[index] = record.target_scalar
        self.__target_multi_class_values[index] = record.target_multi_class
