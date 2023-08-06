"""Module for SweepOperator"""
from typing import Tuple, Iterable

import numpy as np
# pylint: disable=no-name-in-module
from organon.fl.mathematics.sweep.pyx_files.sweep_helper import sweep_fast_row_c, update_row_k

from organon.fl.mathematics.linearalgebra.IBlas import IBlas
from organon.fl.mathematics.sweep.data_classes.swept_attribute import SweptAttribute


class SweepOperator:
    """This is the main part of the algorithm. See sweep operator for further details.
    ftp://public.dhe.ibm.com/software/analytics/spss/support/Stats/Docs/Statistics/Algorithms/13.0/regression.pdf"""

    def __init__(self, matrix: np.ndarray, sigma: np.ndarray, target: int, blas_service: IBlas):
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Input matrix must be square")

        self._matrix = matrix
        self._sigma = sigma
        self._target = target

        self._length = matrix.shape[1]

        self._swept_indices = []
        self._nonswept_indices = []
        self._swept_ever = set()
        self._swept_never = set()
        self._swept_list = []
        self.reset()

        self._tmp_row = np.empty(shape=(self._length,), dtype=np.single)
        self._tmp_col = np.empty(shape=(self._length,), dtype=np.single)
        self.blas_service = blas_service

    def reset(self):
        """Resets sweep related lists."""
        self._swept_indices.clear()
        self._nonswept_indices.clear()
        self._nonswept_indices.extend(range(self._length))
        self._swept_never.update(range(self._length))
        self._nonswept_indices.remove(self._target)
        self._swept_never.remove(self._target)
        self._swept_list.clear()

    def add(self, k: int):
        """Adds element to sweep lists"""
        self._swept_indices.append(k)
        self._nonswept_indices.remove(k)
        self._swept_ever.add(k)
        if k in self._swept_never:
            self._swept_never.remove(k)

    def remove(self, k: int):
        """Removes elements from sweep lists"""
        self._swept_indices.remove(k)
        self._nonswept_indices.append(k)

    def sweep(self, k: int):
        """This is the modified sweep algorithm by Ömer Yılmaz. Still needs improvements. It will be done later.
        Basically it sweeps every attribute is ever swept if the attribute is not in the current swept list.
        Advantage: Reduces the cost of the including the attribute again and sweep the whole matrix again.
        Disadvantage: If an attribute won't be swept ever, this algorithm calculates it also every time."""
        is_in_swept, is_ever_swept = self.find_index_of(k)

        if is_ever_swept:
            # print("row, j = {}, {}".format(row, j))
            # print("Burası")
            attribute = self.get_swept_attribute_before_sweep(k)
            self.sweep_fast_row(self._matrix, k, self._target, self._swept_ever, self._length)
            self.set_swept_attribute_after_sweep(attribute, k)

            if is_in_swept:
                self.remove(k)
            else:
                self.add(k)
            self._swept_list.append(attribute)

        else:
            self.blas_service.scopy(self._length, self._matrix[k, :], 1, self._tmp_row, 1)
            # Operating on columns are a bit tricky via MKL Functions for C_contiguous arrays
            self.blas_service.scopy(self._length, self._matrix.ravel()[k:], self._length, self._tmp_col, 1)
            # self._tmp_col = self._matrix[:, row].copy()

            for attribute in self._swept_list:
                row = attribute.swept_row
                a_row = attribute.unswept_col[k]

                self.blas_service.saxpy(self._length, a_row, row, 1, self._tmp_row, 1)

                col = attribute.swept_col
                a_col = -1.0 * attribute.unswept_row[k]

                self.blas_service.saxpy(self._length, a_col, col, 1, self._tmp_col, 1)

            self.add(k)

            # print(self._tmp_row)
            # print(self._tmp_col)
            for index in self._swept_never:
                self._matrix[k, index] = self._tmp_row[index]
                self._matrix[index, k] = self._tmp_col[index]
            attribute = self.get_swept_attribute_before_sweep(k)
            self.sweep_fast_row(self._matrix, k, self._target, self._swept_ever, self._length)
            self.set_swept_attribute_after_sweep(attribute, k)
            self._swept_list.append(attribute)

    def sweep_old(self, k: int):
        """Old sweep algorithm from .net platform. Whenever an attribute excluded, it resets the matrix and
        calculates again"""
        # for i in range(len(self._swept_list)):
        #    print("i, index = {}, {}".format(i, self._swept_list[i].attribute_index))

        if len(self._swept_list) == 0:
            self.add(k)
            swept_attribute = self.get_swept_attribute_before_sweep(k)
            self.sweep_fast_row(self._matrix, k, self._target, self._swept_indices, self._length)
            self.set_swept_attribute_after_sweep(swept_attribute, k)
            self._swept_list.append(swept_attribute)

        else:
            is_in_swept, _ = self.find_index_of(k)

            if is_in_swept:
                # print("row, j = {}, {}".format(row, j))
                # print("Burası")
                for index in self._swept_indices:
                    self.sweep_fast_row(self._matrix, index, self._target, self._swept_indices, self._length)
                self._swept_indices.remove(k)
                tmp_list = self._swept_indices.copy()
                self.reset()
                for i in tmp_list:
                    self.sweep_old(i)

            else:
                self.blas_service.scopy(self._length, self._matrix[k, :], 1, self._tmp_row, 1)
                # Operating on columns are a bit tricky via MKL Functions for C_contiguous arrays
                self.blas_service.scopy(self._length, self._matrix.ravel()[k:], self._length, self._tmp_col, 1)
                # self._tmp_col = self._matrix[:, row].copy()

                for attribute in self._swept_list:
                    row = attribute.swept_row
                    a_row = attribute.unswept_col[k]

                    self.blas_service.saxpy(self._length, a_row, row, 1, self._tmp_row, 1)

                    col = attribute.swept_col
                    a_col = -1.0 * attribute.unswept_row[k]

                    self.blas_service.saxpy(self._length, a_col, col, 1, self._tmp_col, 1)

                self.add(k)

                # print(self._tmp_row)
                # print(self._tmp_col)

                for index in self._nonswept_indices:
                    self._matrix[k, index] = self._tmp_row[index]
                    self._matrix[index, k] = self._tmp_col[index]
                attribute = self.get_swept_attribute_before_sweep(k)
                self.sweep_fast_row(self._matrix, k, self._target, self._swept_indices, self._length)
                self.set_swept_attribute_after_sweep(attribute, k)
                self._swept_list.append(attribute)

    def get_swept_attribute_before_sweep(self, k: int):
        """Initialize swept attribute with non sweep row and col"""
        row = self._matrix[k, :].copy()
        col = self._matrix[:, k].copy()
        return SweptAttribute(attribute_index=k, unswept_row=row, unswept_col=col)

    def set_swept_attribute_after_sweep(self, attribute: SweptAttribute, k: int):
        """Sets the attribute's swept row and col"""
        attribute.swept_row = self._matrix[k, :].copy()
        attribute.swept_col = self._matrix[:, k].copy()

    def find_index_of(self, k: int) -> Tuple[bool, bool]:
        """Returns if attribute is currently swept, ever swept"""
        for val in self._swept_indices:
            if val == k:
                return True, True

        if k in self._swept_ever:
            return False, True
        return False, False


    def sweep_fast_row(self, matrix: np.ndarray, row: int, target: int, swept: Iterable[int], length: int):
        """Does the sweep algorithm along a row"""
        diag_value = matrix[row, row]
        self.blas_service.sscal(length, -1.0 / diag_value, matrix[row, :], 1)

        for i in range(matrix.shape[0]):
            if i == row:
                continue
            i_value = matrix[i, row]

            if i == target or i in swept:
                self.blas_service.saxpy(length, i_value, matrix[row, :], 1, matrix[i, :], 1)

            else:
                for j in swept:
                    matrix[i, j] += i_value * matrix[row, j]

                matrix[i, target] += i_value * matrix[row, target]
                matrix[i, i] += i_value * matrix[row, i]

            matrix[i, row] = i_value / diag_value
        matrix[row, row] = 1.0 / diag_value

    # @staticmethod
    # def sweep_fast_col(m, row, target, swept, length):
    #     D = m[row, row]
    #     print("m[{0}, {0}] = {1}".format(row, m[row, row]))
    #     print("target =", target)
    #     m_flat = m.ravel()
    #     col_n = m.shape[1]
    #     m[:, row] /= D
    #     swept = list(swept)
    #
    #     for i in range(col_n):
    #         if i == row:
    #             continue
    #         B = -m[row, i]
    #
    #         if i == target or i in swept:
    #             self.blas_service.daxpy(length, B, m_flat[row:], col_n, m_flat[i:], col_n)
    #
    #         else:
    #             self.blas_service.daxpy(len(swept), B, m[swept, row], 1, m[swept, i], 1)
    #
    #         m[row, i] = B / D
    #
    #         if np.isnan(m[1, 1]):
    #             print("{} ise sıkıntı".format(i))
    #     m[row, row] = 1.0 / D


class UnsupervisedSweepOperator:
    """
    Simpler sweep operator for unsupervised feature selection
    """

    def __init__(self, matrix: np.ndarray, blas_service: IBlas):
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Input matrix must be square")

        self._matrix = matrix
        if matrix.dtype not in (np.single, np.double):
            raise ValueError("Input matrix must be single or double")
        self.blas_service = blas_service
        if matrix.dtype.type == np.single:
            self._scal = self.blas_service.sscal
            self._copy = self.blas_service.scopy
            self._axpy = self.blas_service.saxpy
        else:
            self._scal = self.blas_service.dscal
            self._copy = self.blas_service.dcopy
            self._axpy = self.blas_service.daxpy

        self._length = matrix.shape[1]

        self._swept_ever = np.zeros((self._length,), dtype=np.uint8)
        self._swept_never = set(range(self._length))
        self._swept_list = []

        self._tmp_row = np.empty(shape=(self._length,), dtype=matrix.dtype)
        self._tmp_col = np.empty(shape=(self._length,), dtype=matrix.dtype)

    def add(self, k: int):
        """Adds element to sweep lists"""
        self._swept_ever[k] = True
        self._swept_never.remove(k)

    def sweep(self, k: int, num_threads: int):
        """Simpler sweep part"""
        self._tmp_row = np.copy(self._matrix[k, :])
        # self._copy(self._length, self._matrix[k, :], 1, self._tmp_row, 1)
        # Operating on columns are a bit tricky via MKL Functions for C_contiguous arrays
        self._tmp_col = np.copy(self._matrix[:, k])
        # self._copy(self._length, self._matrix.ravel()[k:], self._length, self._tmp_col, 1)
        # self._tmp_col = self._matrix[:, row].copy()

        for attribute in self._swept_list:
            row = attribute.swept_row
            a_row = attribute.unswept_col[k]

            # self._axpy(self._length, a_row, row, 1, self._tmp_row, 1)
            self._tmp_row += a_row * row

            col = attribute.swept_col
            a_col = -1.0 * attribute.unswept_row[k]

            # self._axpy(self._length, a_col, col, 1, self._tmp_col, 1)
            self._tmp_col += a_col * col

        self.add(k)

        # print(self._tmp_row)
        # print(self._tmp_col)
        update_row_k(self._matrix, self._tmp_row, self._tmp_col, self._swept_ever, k, num_threads)
        # for index in self._swept_never:
        #     self._matrix[k, index] = self._tmp_row[index]
        #     self._matrix[index, k] = self._tmp_col[index]
        attribute = self.get_swept_attribute_before_sweep(k)
        # self.sweep_fast_row_targetless(k)
        sweep_fast_row_c(self._matrix, self._length, self._swept_ever, k, num_threads)

        self.set_swept_attribute_after_sweep(attribute, k)
        self._swept_list.append(attribute)

    def get_swept_attribute_before_sweep(self, k: int):
        """Initialize swept attribute with non sweep row and col"""
        # TODO: we can fasten copying process using MKL
        row = self._matrix[k, :].copy()
        col = self._matrix[:, k].copy()
        return SweptAttribute(attribute_index=k, unswept_row=row, unswept_col=col)

    def set_swept_attribute_after_sweep(self, attribute: SweptAttribute, k: int):
        """Sets the attribute's swept row and col"""
        attribute.swept_row = self._matrix[k, :].copy()
        attribute.swept_col = self._matrix[:, k].copy()

    def sweep_fast_row_targetless(self, row: int):
        """Does the sweep algorithm along a row"""
        matrix = self._matrix
        diag_value = matrix[row, row]
        self._scal(self._length, -1.0 / diag_value, matrix[row, :], 1)

        for i in range(matrix.shape[0]):
            if i == row:
                continue
            i_value = matrix[i, row]

            if self._swept_ever[i]:
                self._axpy(self._length, i_value, matrix[row, :], 1, matrix[i, :], 1)

            else:
                for j in range(self._length):
                    if self._swept_ever[j]:
                        matrix[i, j] += i_value * matrix[row, j]
                matrix[i, i] += i_value * matrix[row, i]

            matrix[i, row] = i_value / diag_value
        matrix[row, row] = 1.0 / diag_value

    @property
    def matrix(self):
        """
        Returns the matrix
        :return: matrix
        """
        return self._matrix
