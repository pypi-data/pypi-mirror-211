# pylint: skip-file
"""This module keeps the linear algebra enumerations."""
from enum import Enum
import ctypes
import numpy as np


class SparseOperationT(Enum):
    """Enum for sparse matrix operations."""
    SPARSE_OPERATION_NON_TRANSPOSE = 10
    SPARSE_OPERATION_TRANSPOSE = 11
    SPARSE_OPERATION_CONJUGATE_TRANSPOSE = 12


class SparseIndexBaseT(Enum):
    """Enum for sparse matrix index base."""
    SPARSE_INDEX_BASE_ZERO = 0
    SPARSE_INDEX_BASE_ONE = 1


class SparseStatusT(Enum):
    """Enum for sparse matrix operations status."""
    SPARSE_STATUS_SUCCESS = 0
    SPARSE_STATUS_NOT_INITIALIZED = 1
    SPARSE_STATUS_ALLOC_FAILED = 2
    SPARSE_STATUS_INVALID_VALUE = 3
    SPARSE_STATUS_EXECUTION_FAILED = 4
    SPARSE_STATUS_INTERNAL_ERROR = 5
    SPARSE_STATUS_NOT_SUPPORTED = 6


class SparseLayoutT(Enum):
    """Enum for sparse matrix layout type."""
    SPARSE_LAYOUT_ROW_MAJOR = 101
    SPARSE_LAYOUT_COLUMN_MAJOR = 102


class SparseMatrix(ctypes.Structure):
    """Enum for sparse matrix."""


class MatrixDescr(ctypes.Structure):
    """Enum for matrix description."""
    _fields_ = [('type', ctypes.c_int),
                ('mode', ctypes.c_int),
                ('diag', ctypes.c_int)]


descr = MatrixDescr()
descr.type = ctypes.c_int(20)
descr.mode = ctypes.c_int(42)
descr.diag = ctypes.c_int(50)

sparse_matrix_t = ctypes.POINTER(SparseMatrix)

matdescrA = np.chararray((4,))
matdescrA[0] = 'G'
matdescrA[1] = 'L'
matdescrA[2] = 'N'
matdescrA[3] = 'C'

transA = ctypes.c_char_p(b'n')
