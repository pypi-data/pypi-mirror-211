"""Module for DenseMatrix"""
import numpy as np
from organon.fl.mathematics.sweep.matrices.i_matrix import IMatrix


class DenseMatrix(IMatrix):
    """Matrix class for dense matrices"""

    @property
    def is_centralized(self):
        """Get the centralized information"""
        return self._is_centralized

    @property
    def data(self):
        """Get the data"""
        return self._data

    @property
    def shape(self):
        """Get the shape of the matrix"""
        return self._shape

    @property
    def means(self) -> np.ndarray:
        """Get the column means of the matrix"""
        return self._means

    def __init__(self, data: np.ndarray):
        if len(data.shape) != 2:
            raise ValueError("Array should be 2 dimensional")
        self._data = data
        self._shape = data.shape
        self._means = np.mean(data, axis=0)

        self.centralize_columns()
        self._check_centralized()

    def _check_centralized(self):
        """Check if the matrix centralized"""
        self._is_centralized = True

        for j in range(self.shape[1]):
            if ~np.isclose(np.mean(self._data[:, j]), 0):
                self._is_centralized = False

    def get_column(self, k: int):
        """Get specified column of the matrix"""
        return self._data[:, k].copy()

    def centralize_columns(self):
        """Centralize all columns"""
        self._data -= np.mean(self._data, axis=0)

        self._is_centralized = True

    def mul_vector(self, vector: np.ndarray):
        """Calculates Matrix Vector product"""
        return np.dot(self._data.T, vector)
