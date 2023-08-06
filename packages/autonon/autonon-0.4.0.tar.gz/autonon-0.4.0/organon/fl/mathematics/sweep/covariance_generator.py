"""Module for CovarianceGenerator"""
from typing import List

import numpy as np
# pylint: disable=no-name-in-module
from organon.fl.mathematics.sweep.pyx_files.sweep_helper import compute_covariances_c

from organon.fl.mathematics.linearalgebra.IBlas import IBlas
from organon.fl.mathematics.sweep.covariance_info import CovarianceInfo
from organon.fl.mathematics.sweep.data_classes.transformation import Transformation
from organon.fl.mathematics.sweep.matrices.csc_matrix import CscMatrix
from organon.fl.mathematics.sweep.matrices.dense_matrix import DenseMatrix
from organon.fl.mathematics.sweep.matrices.i_matrix import IMatrix


class CovarianceGenerator:
    """Class for JIT CovarianceGenerator. Firstly calculates diagonals of covariance and correlation
    matrices. After that calculates the corresponding columns and rows of the matrices."""

    @property
    def covariance_info(self):
        """Get the covariance info"""
        return self._covariance_info

    @property
    def biased(self):
        """Get the bias info"""
        return self._biased

    def __init__(self, biased: bool, matrix: IMatrix, transformations: List[Transformation], weight_column: np.ndarray,
                 blas_service: IBlas):
        self.validate(matrix, transformations, weight_column)

        self._biased = biased
        self._matrix = matrix
        if matrix.data.dtype.type == np.float32:
            self.dot = blas_service.sdot
        else:
            self.dot = blas_service.ddot

        self._variable_count = self._matrix.shape[1]
        # self._indices = indices
        self._transformations = transformations
        self._weight_column = weight_column

        self._is_computed = np.zeros((self._variable_count,), dtype=np.uint8)

        self._covariance_info: CovarianceInfo = None

    @staticmethod
    def validate(matrix: IMatrix, transformations: List[Transformation], weight_column: np.ndarray):
        """Validate the matrix, transformations and weight column"""
        if matrix is None:
            raise ValueError("Matrix can not be None as input to JitCovarianceMatrixGenerator")
        if transformations is None:
            raise ValueError("Transformations can not be None as input to JitCovarianceMatrixGenerator")
        if weight_column is None:
            raise ValueError("Weight_column can not be None as input to JitCovarianceMatrixGenerator")
        if weight_column.shape[0] != matrix.shape[1]:
            raise ValueError(f"Matrix shape and Weight Column shape don't fit. "
                             f"weight_column.shape = {weight_column.shape}, matrix.shape = {matrix.shape}")

    def initialize(self):
        """initialize the covariance info using covariance matrix and dimension"""
        dim = self._variable_count

        self._matrix.data[:] = CovarianceGenerator.get_transformed_array(self._matrix.data, self._transformations[0])

        matrix = np.empty(shape=(dim, dim), dtype=self._matrix.data.dtype)
        matrix.fill(float('nan'))
        covariance_matrix = matrix
        self._covariance_info = CovarianceInfo(covariance_matrix, dim)

    @staticmethod
    def get_transformed_array(inp, transformation: Transformation) -> np.ndarray:
        """Apply transformation to input"""
        return np.array([transformation.evaluate(item) for item in inp])

    def compute_variances(self):
        """Calculates diagonals of correlation and covariance matrix"""
        sigma = self._covariance_info.covariance_matrix
        corr_matrix = self._covariance_info.correlation_matrix
        for i in range(self._variable_count):
            if ~np.isnan(sigma[i, i]):
                continue
            col_i = self._matrix.get_column(i)
            variance = self.dot(self._matrix.shape[0], col_i, 1, col_i, 1)
            variance /= self._matrix.shape[0] - 1

            sigma[i, i] = variance
            corr_matrix[i, i] = 1.0

    def compute_covariances_c(self, variable: int, n_thread: int, bin_size: int):
        """
        Compute Covariance using Cython
        """
        compute_covariances_c(self._matrix,
                              self._matrix.means,
                              self._covariance_info.covariance_matrix,
                              self._covariance_info.correlation_matrix,
                              self._is_computed,
                              variable,
                              bin_size,
                              n_thread)

    def compute_covariances(self, variable: int):
        """Computes covariances of @variable and other elements
        This method computes covariances JIT."""
        sigma = self._covariance_info.covariance_matrix
        corr_matrix = self._covariance_info.correlation_matrix

        col_variable = self._matrix.get_column(variable)

        if isinstance(self._matrix, DenseMatrix):
            covariances = self._matrix.mul_vector(col_variable)
        elif isinstance(self._matrix, CscMatrix):
            dense_m = self._matrix.to_dense()
            dense_m -= np.mean(dense_m, axis=0)
            covariances = np.dot(dense_m.T, col_variable)
        else:
            raise NotImplementedError
        covariances /= self._matrix.shape[0] - 1
        i = variable

        for j in range(self._variable_count):
            if self._is_computed[j]:
                continue
            if ~np.isnan(sigma[i, j]):
                continue

            sigma[i, j] = sigma[j, i] = covariances[j]

            nan_i = np.isnan(sigma[i, i])
            zero_i = sigma[i, i] <= 0

            if i == j:
                corr_matrix[i, i] = float('nan') if nan_i else 1.0
            else:
                nan_j = np.isnan(sigma[j, j])
                zero_j = sigma[j, j] <= 0

                if np.isnan(sigma[i, j]) or nan_i or nan_j:
                    corr_matrix[i, j] = float('nan')

                elif zero_i or zero_j:
                    corr_matrix[i, j] = 0.0

                else:
                    corr_matrix[i, j] = sigma[i, j] / np.sqrt(sigma[i, i] * sigma[j, j])

                corr_matrix[j, i] = corr_matrix[i, j]

    def add(self, variable):
        """Adds a variable to calculated variables"""
        self._is_computed[variable] = True

    def get_density(self):
        """Returns density(not empty elements) of the covariance matrix"""
        sigma = self._covariance_info.covariance_matrix
        return np.count_nonzero(~np.isnan(sigma)) / sigma.size
