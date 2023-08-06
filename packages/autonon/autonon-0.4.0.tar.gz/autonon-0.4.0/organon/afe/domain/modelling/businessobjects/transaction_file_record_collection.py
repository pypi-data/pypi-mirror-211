"""
This module includes TransactionFileRecordCollection class.
"""
from typing import Dict

import numpy as np

from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats


class TransactionFileRecordCollection:
    """
    Collection of transaction file records
    """

    # pylint: disable=unused-argument
    def __init__(self, date_col_map: Dict[str, int], d_map: Dict[str, int], q_map: Dict[str, int],
                 max_record_count: int):
        super().__init__()
        self.transaction_file_stats: TransactionFileStats = None
        self.__date_col_map: Dict[str, int] = date_col_map
        self.__d_map: Dict[str, int] = d_map
        self.__q_map: Dict[str, int] = q_map
        self.__entity_index_map: Dict[str, np.array] = {}
        self.__dates: np.ndarray = np.full([max_record_count, len(date_col_map)], -1, dtype=np.int64)
        self.__q_arrays: np.ndarray = np.full([max_record_count, len(q_map)], None, dtype=np.float32)
        self.__d_arrays: np.ndarray = np.full([max_record_count, len(d_map)], -1, dtype=np.int8)

        self.__last_filled_index: int = None
        self.max_record_count = max_record_count

    @property
    def actual_record_count(self) -> int:
        """Number of rows that was filled with data.(Ignoring rows with dummy data)"""
        if self.__last_filled_index is None:
            return 0
        return self.__last_filled_index + 1

    @property
    def entity_index_map(self) -> Dict[str, np.array]:
        """Map of indices corresponding to given entity'"""
        return self.__entity_index_map

    @property
    def dates(self) -> np.ndarray:
        """Dates in transaction file records"""
        return self.__dates

    @property
    def d_arrays(self) -> np.ndarray:
        """Dimension values in transaction file records"""
        return self.__d_arrays

    @property
    def q_arrays(self) -> np.ndarray:
        """Quantity values in transaction file records"""
        return self.__q_arrays

    @property
    def date_col_map(self) -> Dict[str, int]:
        """Returns value of private attribute '__date_col_map'"""
        return self.__date_col_map

    @property
    def d_map(self) -> Dict[str, int]:
        """Returns value of private attribute '__d_map'"""
        return self.__d_map

    @property
    def q_map(self) -> Dict[str, int]:
        """Returns value of private attribute '__q_map'"""
        return self.__q_map

    def sort(self, date_column_name: str):
        """Sorts every list of transaction file records"""
        date_col_index = self.__date_col_map[date_column_name]
        new_entity_index_map = {}
        for entity, indices in self.__entity_index_map.items():
            indices_list: list = indices.tolist()
            new_entity_index_map[entity] = np.array(sorted(indices_list,
                                                           key=lambda _index: self.__dates[_index][date_col_index],
                                                           reverse=True), dtype=np.int32)
        self.__entity_index_map = new_entity_index_map

    def append(self, entity_id: str, trx_date_array: list, q_array: list, d_array: list):
        """Appends given transaction file record information to collection"""
        if self.__last_filled_index is None:
            self.__last_filled_index = -1
        self.__last_filled_index += 1
        index = self.__last_filled_index

        self.__dates[index] = trx_date_array
        self.__q_arrays[index] = q_array
        self.__d_arrays[index] = d_array

        if entity_id in self.__entity_index_map:  # bu kontrol her zaman olmalı
            self.__entity_index_map[entity_id].append(index)
        else:
            self.__entity_index_map[entity_id] = [index]

    def convert_entity_index_lists_to_array(self):
        """Converts entity index map values to numpy arrays"""
        for entity, index_list in self.__entity_index_map.items():
            if isinstance(index_list, list):
                self.__entity_index_map[entity] = np.array(index_list, dtype=np.int32)
