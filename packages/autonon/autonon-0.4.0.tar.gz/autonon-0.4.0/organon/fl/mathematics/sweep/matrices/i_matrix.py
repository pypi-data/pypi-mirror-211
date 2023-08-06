"""Module for IMatrix"""
from abc import ABCMeta, abstractmethod
import numpy as np


class IMatrix(metaclass=ABCMeta):
    """Matrix interface for sweep algorithm"""
    @property
    @abstractmethod
    def shape(self) -> tuple:
        """Shape of the matrix"""

    @property
    @abstractmethod
    def is_centralized(self) -> bool:
        """Get the centralized information"""

    @property
    @abstractmethod
    def data(self) -> np.ndarray:
        """Get the data"""

    @property
    @abstractmethod
    def means(self) -> np.ndarray:
        """Get column means of the matrix"""

    @abstractmethod
    def get_column(self, k: int) -> np.ndarray:
        """Get specified column of the matrix"""

    @abstractmethod
    def mul_vector(self, vector: np.ndarray) -> np.ndarray:
        """Calculates Matrix Vector product"""

    @abstractmethod
    def centralize_columns(self):
        """Centralize all columns"""
