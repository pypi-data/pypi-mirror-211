"""Module for CscMatrix"""
import numpy as np
from organon.fl.mathematics.linearalgebra.MklFunctions import MklFunctions
from organon.fl.mathematics.linearalgebra.enums import descr, SparseOperationT
from organon.fl.mathematics.sweep.matrices.i_matrix import IMatrix


class CscMatrix(IMatrix):
    """Double Csr matrix for sparse matrices"""
    @property
    def data(self) -> np.ndarray:
        """Get the data"""
        return self._data

    @property
    def col_ptr(self) -> np.ndarray:
        """Get col ptr"""
        return self._col_ptr

    @property
    def row_ptr(self) -> np.ndarray:
        """Get the row ptr"""
        return self._row_ptr

    @property
    def shape(self) -> tuple:
        """Get the shape of matrix"""
        return self._shape

    @property
    def means(self) -> np.ndarray:
        """Get column means of the matrix"""
        return self._means

    @property
    def is_centralized(self) -> bool:
        """Get the centralized information"""
        return self._is_centralized

    def __init__(self, data: np.ndarray, row_ptr: np.ndarray, col_ptr: np.ndarray, shape: tuple = None):

        CscMatrix.validate(data, row_ptr, col_ptr, shape)

        self._nnz = data.size
        self._data = data
        self._row_ptr = row_ptr
        self._col_ptr = col_ptr

        if shape is not None:
            self._shape = shape
        else:
            self._shape = (max(row_ptr) + 1, col_ptr.size - 1)

        self._means = np.empty(self._shape[1], dtype=data.dtype)
        self._calculate_means()

        self._is_centralized = False

    def _calculate_means(self):
        for i in range(self._shape[1]):
            start = self._col_ptr[i]
            end = self._col_ptr[i + 1]
            self._means[i] = np.sum(self._data[start:end])
        self._means /= self._shape[0]

    @staticmethod
    def validate(data: np.ndarray, row_ptr: np.ndarray, col_ptr: np.ndarray, shape: tuple):
        """Validates the parameters"""
        if data is None or row_ptr is None or col_ptr is None:
            raise ValueError("Arrays should be defined")

        if data.dtype.type not in (np.single, np.double):
            raise ValueError("Data Type must be single or double")

        if row_ptr.size != data.size:
            raise ValueError("data size and col_ptr size are incompatible")

        if col_ptr[-1] != data.size:
            raise ValueError("col_ptr[-1] and NNZ are incompatible")

        if shape is not None:
            if len(shape) != 2:
                raise ValueError("Array must be 2 dimensional")
            if shape[1] != col_ptr.size - 1:
                raise ValueError("Column count and col_ptr size are incompatible")

            if shape[0] < max(row_ptr) + 1:
                raise ValueError("Row count and row_ptr elements are incompatible")

    def get_column(self, k: int) -> np.ndarray:
        """Get specified column of the matrix"""
        column_array = np.zeros(self._shape[0], dtype=self._data.dtype)

        start = self._col_ptr[k]
        end = self._col_ptr[k + 1]

        column_array[self._row_ptr[start:end]] = self._data[start:end]

        return column_array

    def centralize_columns(self):
        """Centralize all columns"""

    def to_dense(self) -> np.ndarray:
        """Convert sparse matrix to dense matrix"""
        dense_matrix = np.zeros(shape=self._shape, dtype=self._data.dtype)

        for j in range(len(self._col_ptr) - 1):
            start = self._col_ptr[j]
            end = self._col_ptr[j + 1]

            for i in range(start, end):
                dense_matrix[self._row_ptr[i], j] = self._data[i]

        return dense_matrix

    def mul_vector(self, vector: np.ndarray) -> np.ndarray:
        """Calculates Matrix Vector product"""
        dtype = self._data.dtype
        result = np.zeros(shape=self._shape[1], dtype=dtype)
        if dtype.type is np.single:
            MklFunctions.sparse_s_mv(SparseOperationT.SPARSE_OPERATION_TRANSPOSE, self._shape[0], self._shape[1],
                                     np.single(1.0),
                                     descr, self._data, self._row_ptr,
                                     self._col_ptr[0:-1],
                                     self._col_ptr[1:], vector, np.single(1.0), result, sparse_format='csc')
        else:
            MklFunctions.sparse_d_mv(SparseOperationT.SPARSE_OPERATION_TRANSPOSE, self._shape[0], self._shape[1],
                                     np.double(1.0),
                                     descr, self._data, self._row_ptr,
                                     self._col_ptr[0:-1],
                                     self._col_ptr[1:], vector, np.double(1.0), result, sparse_format='csc')
        return result
