# pylint: skip-file

# cython: cdivision=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: language_level=3
# cython: profile=True

from cython.parallel import prange
import numpy as np
cimport numpy as np
from libc.math cimport isnan, sqrt, NAN
from organon.fl.mathematics.sweep.matrices.i_matrix import IMatrix


ctypedef np.uint8_t uint8


def update_row_k(float[:, :] matrix,
                 float[:] tmp_row,
                 float[:] tmp_col,
                 uint8[:] swept_ever,
                 int k,
                 int n_threads):
    """Updates row for new added feature"""
    cdef int index

    for index in prange(swept_ever.shape[0], nogil=True, num_threads=n_threads):
        if not swept_ever[index]:
            matrix[k, index] = tmp_row[index]
            matrix[index, k] = tmp_col[index]



def sweep_fast_row_c(np.ndarray[float, ndim=2] np_matrix, int length, uint8[:] swept_ever, int row, int n_threads):
    """Does the sweep algorithm along a row"""
    cdef:
        float[:, :] matrix = np_matrix
        float diag_value = matrix[row, row]
        int i, j
        float i_value
    np_matrix[row, :] /= -diag_value

    for i in prange(matrix.shape[0], nogil=True, num_threads=n_threads):
        if i == row:
            continue
        i_value = matrix[i, row]
        # If feature i is swept then we have all the row
        if swept_ever[i]:
            with gil:
                np_matrix[i, :] += i_value * np_matrix[row, :]
            # MklFunctions.daxpy(length, i_value, np.asarray(matrix[row, :]), 1, np.asarray(matrix[i, :]), 1)
        # If not then we have to do operations along the swept indices
        else:
            for j in range(length):
                if swept_ever[j]:
                    matrix[i, j] += i_value * matrix[row, j]
            matrix[i, i] += i_value * matrix[row, i]

        matrix[i, row] = i_value / diag_value
    matrix[row, row] = 1.0 / diag_value

def get_correlation_matrix_c(float[:, :] covariance_matrix, int n_threads) -> np.ndarray:
    """Gets correlation matrix from covariance matrix"""
    cdef:
        float[:, :] matrix = covariance_matrix
        int rows = matrix.shape[0]
        int cols = matrix.shape[1]
        int i, j
        bint nan_i, nan_j, zero_i, zero_j
        float[:, :] sigma = np.empty(shape=(rows, cols), dtype=np.single)

    # This loop checks the covariance matrix. If it can calculate some index of correlation matrix then calculates.
    for i in prange(rows, nogil=True, num_threads=n_threads):
        nan_i = isnan(matrix[i, i])
        zero_i = matrix[i, i] <= 0

        sigma[i, i] = NAN if nan_i else 1.0

        for j in range(i, cols):
            nan_j = isnan(matrix[j, j])
            zero_j = matrix[j, j] <= 0

            if isnan(matrix[i, j]) or nan_i or nan_j:
                sigma[i, j] = NAN

            elif zero_i or zero_j:
                sigma[i, j] = 0.0

            else:
                sigma[i, j] = matrix[i, j] / sqrt(matrix[i, i] * matrix[j, j])

            sigma[j, i] = sigma[i, j]

    return np.asarray(sigma)


def compute_covariances_c(matrix: IMatrix,
                               float[:] means,
                               float[:, :] sigma,
                               float[:, :] corr_matrix,
                               uint8[:] is_computed,
                               int variable,
                               int bin_size,
                               int n_threads):
    """Computes covariances of @variable and other elements
    This method computes covariances JIT. Since we split main
     frame to bins this computes all the bins for a variable.
     As can see from https://en.wikipedia.org/wiki/Covariance
     covariance is normalized dot product of vectors(divided by length)
     Using these covariances we compute the correlations."""

    cdef:
        float[:, :] covariances
        np.ndarray[float, ndim=2] norm_col_variable
        np.ndarray[float, ndim=2] norm_col_i
        long long[:] col_ptr = matrix.col_ptr
        long long[:] row_ptr = matrix.row_ptr
        int i, j, start, end
        bint nan_i, nan_j, zero_i, zero_j
        np.ndarray[float, ndim=2] np_covariances = np.empty(shape=(matrix.shape[1], bin_size), dtype=np.single)

    # First get normalized feature[variable]. Since we have bins get all of them.
    start = variable * bin_size
    end = start + bin_size
    norm_col_variable = get_columns_normalized(matrix.shape[0], start, end, col_ptr, row_ptr, means, n_threads)

    # We need to compute normalization of all features. However normalized feature cannot be sparse anymore.
    # For example: [1, 0, 0, 0] -> [3/4, -1/4, -1/4, -1/4]
    # As you can see there is no zero value in output feature. Therefore we need dense matrix for all features.
    # However we cannot put all matrix into dense matrix due to memory constraints.
    # We split matrix to batches and put these features to dense matrix and compute the dot product of these features
    # via matrix multiplication.
    for i in range(0, matrix.shape[1], bin_size):
        norm_col_i = get_columns_normalized(matrix.shape[0], i, i + bin_size, col_ptr, row_ptr, means, n_threads)
        np_covariances[i:i+bin_size] = np.dot(norm_col_i.T, norm_col_variable)

    # Divide by length
    np_covariances /= (matrix.shape[0] - 1)
    # Get memory view of numpy array to use in nogil section.
    covariances = np_covariances
    # For loop over variables to be computed
    for i in range(start, end):
        # For variable i calculate correlation[i, j] can be done parallel
        for j in prange(is_computed.shape[0], nogil=True, num_threads=n_threads):
            if is_computed[j]:
                continue
            if not isnan(sigma[i, j]):
                continue

            sigma[i, j] = covariances[j, i-start]
            sigma[j, i] = covariances[j, i-start]

            nan_i = isnan(sigma[i, i])
            zero_i = sigma[i, i] <= 0

            if i == j:
                corr_matrix[i, i] = NAN if nan_i else 1.0
            else:
                nan_j = isnan(sigma[j, j])
                zero_j = sigma[j, j] <= 0

                if isnan(sigma[i, j]) or nan_i or nan_j:
                    corr_matrix[i, j] = NAN

                elif zero_i or zero_j:
                    corr_matrix[i, j] = 0.0

                else:
                    corr_matrix[i, j] = sigma[i, j] / sqrt(sigma[i, i] * sigma[j, j])

                corr_matrix[j, i] = corr_matrix[i, j]
        is_computed[i] = True

cdef np.ndarray[float, ndim=2] get_columns_normalized(int row,
                                                      int col_start,
                                                      int col_end,
                                                      long long[:] col_ptr,
                                                      long long[:] row_ptr,
                                                      float[:] means,
                                                      int n_threads):
    """Convert sparse matrix columns to dense matrix"""
    cdef:
        np.ndarray[float, ndim=2] dense_matrix = np.zeros(shape=(row, col_end-col_start), dtype=np.single)
        int start, end, i, j
    # To understand this conversion, see CSC matrix format. Basically slice columns from col_start to col_end
    for j in prange(col_start, col_end, nogil=True, num_threads=n_threads):
        start = col_ptr[j]
        end = col_ptr[j + 1]

        for i in range(start, end):
            # Since we split binary bins. We now that all data is 1.0
            dense_matrix[row_ptr[i], j-col_start] = 1.0

    # Normalize columns.
    dense_matrix -= means.base[col_start:col_end]

    return dense_matrix

