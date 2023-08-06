"""Includes DataPartition class."""
import random
from typing import List

import numpy as np

from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.core.businessobjects.idata_partition import IDataPartition
from organon.fl.mathematics.businessobjects.tuple_generic_collection import TupleGenericCollection

epsilon_val = np.finfo(float).eps


class DataPartition(IDataPartition):
    """This class helps with partitioning a dataframe according to training settings."""

    def __init__(self, frame: IDataFrame = None):
        super().__init__()
        self.__frame: IDataFrame = frame
        self.__training_ratio: float = 1.0
        self.__training_indices: List[int] = None
        self.__validation_indices: List[int] = None
        self.__strata_info: TupleGenericCollection[int] = None

    @property
    def frame(self):
        return self.__frame

    @property
    def training_ratio(self):
        return self.__training_ratio

    @property
    def validation_ratio(self):
        """Returns ratio of validation (1.0 - training ratio)"""
        return 1.0 - self.__training_ratio

    @property
    def strata_info(self):
        return self.__strata_info

    @property
    def training_indices(self) -> List[int]:
        return self.__training_indices

    @training_indices.setter
    def training_indices(self, value):
        self.__training_indices = value

    @property
    def validation_indices(self) -> List[int]:
        return self.__validation_indices

    @validation_indices.setter
    def validation_indices(self, value):
        self.validation_indices = value

    def partition(self, training_ratio: float = 1.0):
        system_random = random.SystemRandom()
        rows = self.__frame.row_count
        if epsilon_val < training_ratio <= 1.0:
            self.__training_ratio = training_ratio
            if self.__training_ratio >= 1.0:
                self.__training_indices = list(range(rows))
            else:
                t_list = []
                v_list = []
                for i in range(rows):
                    if system_random.uniform(0, 1) <= self.__training_ratio:
                        t_list.append(i)
                    else:
                        v_list.append(i)
                self.__training_indices = t_list
                self.__validation_indices = v_list
        else:
            self.__training_ratio = 1.0
            self.__training_indices = list(range(rows))

    def set_frame(self, frame: IDataFrame):
        """Changes frame of the partition"""
        self.__frame = frame
