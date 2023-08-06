"""Module Description"""
import numpy as np
# pylint: disable=no-name-in-module
from organon.fl.mathematics.sweep.pyx_files.sweep_helper import get_correlation_matrix_c


class CovarianceInfo:
    """Class Description"""
    @property
    def correlation_matrix(self):
        """Get the correlation matrix"""
        return self._correlation_matrix

    @property
    def covariance_matrix(self):
        """Get the covariance matrix"""
        return self._covariance_matrix

    @property
    def means(self):
        """Get the means"""
        return self._means

    @property
    def total_case_weight(self):
        """Get the total case weight"""
        return self._total_case_weight

    def __init__(self, covariance_matrix: np.ndarray, total_case_weight: int):
        CovarianceInfo._validate(covariance_matrix, total_case_weight)
        self._covariance_matrix = covariance_matrix
        # self._correlation_matrix = CovarianceInfo.get_correlation_matrix(covariance_matrix)
        self._correlation_matrix = get_correlation_matrix_c(covariance_matrix, 4)

        self._means = np.empty(shape=(covariance_matrix.shape[0],), dtype=self._covariance_matrix.dtype)
        self._means.fill(float('nan'))

        self._total_case_weight = total_case_weight

    @staticmethod
    def _validate(covariance_matrix: np.ndarray, total_case_weight: int):
        """Validates input elements"""
        if covariance_matrix is None:
            raise ValueError("Covariance matrix can not be null in CovarianceInfo constructor.")

        if covariance_matrix.shape[0] != covariance_matrix.shape[1]:
            raise ValueError("Covariance matrix must be a square matrix.")

        if total_case_weight <= 0:
            raise ValueError("TotalCaseWight must be positive in CovarianceInfo constructor.")

    def update_correlation_matrix(self):
        """Updates correlation matrix according to covariance matrix."""
        self._correlation_matrix = CovarianceInfo.get_correlation_matrix(self._covariance_matrix)

    @staticmethod
    def get_correlation_matrix(covariance_matrix: np.ndarray) -> np.ndarray:
        """Gets correlation matrix from covariance matrix"""
        matrix = covariance_matrix
        rows = matrix.shape[0]
        cols = matrix.shape[1]

        if rows != cols:
            raise ValueError("Covariance shape doesn't fit for getting correlation matrix."
                             f" Rows = {rows}, Cols = {cols}")

        sigma = np.empty(shape=(rows, cols), dtype=matrix.dtype)

        for i in range(rows):
            nan_i = np.isnan(matrix[i, i])
            zero_i = matrix[i, i] <= 0

            sigma[i, i] = float('nan') if nan_i else 1.0

            for j in range(i, cols):
                nan_j = np.isnan(matrix[j, j])
                zero_j = matrix[j, j] <= 0

                if np.isnan(matrix[i, j]) or nan_i or nan_j:
                    sigma[i, j] = float('nan')

                elif zero_i or zero_j:
                    sigma[i, j] = 0.0

                else:
                    sigma[i, j] = matrix[i, j] / np.sqrt(matrix[i, i] * matrix[j, j])

                sigma[j, i] = sigma[i, j]

        return sigma

    def get_non_zero_variance_attributes(self) -> set:
        """Returns non zero variance attributes"""
        indices = set()

        for i in range(self._covariance_matrix.shape[0]):
            variance = self._covariance_matrix[i, i]

            if np.isnan(variance) or variance <= 0:
                continue
            indices.add(i)

        return indices

    def get_variances(self, linear_form) -> float:
        """Returns variances for matrix * linear_form(vector) multiplication"""
        rows = self._covariance_matrix.shape[0]

        if any(key >= rows for key in linear_form):
            raise IndexError("At least one variable in the linear form does not correspond to covariance matrix"
                             " variables")

        variance = 0.0

        for i in linear_form:
            beta_i = linear_form[i]
            for j in linear_form:
                beta_j = linear_form[j]
                variance += beta_i * beta_j * self._covariance_matrix[i, j]

        return variance

    def get_covariances(self, linear_form, target) -> float:
        """Calculates covariance of matrix vector product"""
        rows = self._covariance_matrix.shape[0]

        if any(key >= rows for key in linear_form):
            raise IndexError("At least one variable in the linear form does not correspond to covariance matrix"
                             " variables")
        if target >= rows:
            raise IndexError("The target variable does not correspond to any covariance matrix variable")

        variance = 0.0
        for i in linear_form:
            beta_i = linear_form[i]
            variance += beta_i * self._covariance_matrix[i, target]

        return variance
