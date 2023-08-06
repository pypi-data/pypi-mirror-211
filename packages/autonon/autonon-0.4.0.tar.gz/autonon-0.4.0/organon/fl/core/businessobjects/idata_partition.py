"""Includes IDataPartition(base class for data partitioning classes) class."""
import abc
from typing import List

from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.mathematics.businessobjects.tuple_generic_collection import TupleGenericCollection


class IDataPartition(metaclass=abc.ABCMeta):
    """Abstract base class for classes for data partitioning."""

    @property
    @abc.abstractmethod
    def frame(self) -> IDataFrame:
        """Returns the dataframe."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def training_ratio(self) -> float:
        """Returns the approximate value of 'size of training data/ size of all data'"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def training_indices(self) -> List[int]:
        """Indices of rows which will be used as training data."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def validation_indices(self) -> List[int]:
        """Indices of rows which will be used as validation data."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def strata_info(self) -> TupleGenericCollection[int]:
        """strata_info for partition"""
        raise NotImplementedError

    @abc.abstractmethod
    def partition(self, training_ratio: float):
        """Generates random training and validation indices according to training ratio."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_frame(self, frame: IDataFrame):
        """Changes frame of the partition"""
        raise NotImplementedError
