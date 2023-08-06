"""Includes UnsupervisedFeatureExtractor class."""
import random
import sys
from typing import Optional, List, Tuple, Dict

import numpy as np
from scipy.sparse import csc_matrix

from organon.fl.core.executionutil.objects.stopwatch import StopWatch
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.fl.mathematics.linearalgebra.blas_service_factory import BlasServiceFactory
from organon.fl.mathematics.sweep.covariance_generator import CovarianceGenerator
from organon.fl.mathematics.sweep.data_classes.transformation import Transformation
from organon.fl.mathematics.sweep.matrices.csc_matrix import CscMatrix
from organon.fl.mathematics.sweep.sweep_operator import UnsupervisedSweepOperator


class UnsupervisedFeatureExtractor:
    """
    Class for Unsupervised Feature Extraction Algorithm.
    """

    def __init__(self, data_frame: Dict[str, np.ndarray], bin_count: int = 4, r_factor: float = 0.9,
                 random_state: int = None, max_iter: int = 500,
                 is_logging: bool = False):
        self.__frame = data_frame
        self.__bin_count = bin_count
        self.__r_limit = bin_count * r_factor
        self.__random_state = random_state
        self.__max_iter = max_iter
        if max_iter < 0:
            self.__max_iter = sys.maxsize
        self.__is_logging = is_logging

        self.__un_swept = None
        self.__operator = None
        self.__generator = None
        self.__cov_info = None

    def log(self, log_str):
        """
        Logs the input str if logging is enables
        :param log_str: input str
        :return: None
        """
        if self.__is_logging:
            LogHelper.info(log_str)

    def execute(self, num_threads: int):
        """
            This is the main function.
            :param num_threads: number of parallel threads
            :return: None for now
            """
        watch = StopWatch()
        watch.start()
        input_frame, index_to_name = self.get_sparse_frame()

        if input_frame is None:
            return []

        self.log(f"Sparse Frame is Created in {watch.get_elapsed_seconds(True)}")

        random.seed(self.__random_state)
        first_enter = random.randrange(0, len(index_to_name))  # nosec
        self.log(index_to_name[first_enter])
        self.__un_swept = set(range(len(index_to_name)))

        sweep_operator, generator = self.get_sweep_operator_generator(input_frame)
        self.__operator = sweep_operator
        self.__generator = generator
        self.__cov_info = generator.covariance_info
        self.log(f"Sweep Operator and Cov Generator initialized in {watch.get_elapsed_seconds(True)}")

        self.include(first_enter, num_threads)

        for _ in range(self.__max_iter):
            if len(self.__un_swept) == 0:
                break

            next_swept = self.get_next_swept()

            if next_swept is None:
                break

            if next_swept[1] < self.__r_limit:
                break
            self.log(f'{index_to_name[next_swept[0]], next_swept[1]}')

            next_col = next_swept[0]
            self.include(next_col, num_threads)

        swept = set(range(len(index_to_name))).difference(self.__un_swept)
        # print(f'{swept=}')
        # print(f'{un_swept=}')
        return [index_to_name[index] for index in swept]

    def include(self, feature: int, num_threads: int):
        """
        Includes a feature via calculating correlation and sweeping.
        :param feature: Include feature
        :param num_threads: number of threads for parallel processing
        :return: None
        """
        bin_count = self.__bin_count
        self.__generator.compute_covariances_c(feature, num_threads, bin_count)
        start = feature * bin_count
        end = start + bin_count
        for col_extended in range(start, end):
            self.__operator.sweep(col_extended, num_threads)
        self.__un_swept.remove(feature)

    def get_next_swept(self) -> (int, float):
        """
        Gets next feature to sweep
        :return: index and value of a feature
        """
        bin_count = self.__bin_count
        next_swept: Optional[Tuple] = None

        for col in self.__un_swept:
            corr_tot = 0
            start = col * bin_count
            end = start + bin_count
            for i in range(start, end):
                corr_tot += self.__cov_info.correlation_matrix[i, i]

            if next_swept is None:
                next_swept = (col, corr_tot)
            elif corr_tot > next_swept[1]:  # pylint: disable=(unsubscriptable-object)
                next_swept = (col, corr_tot)

        return next_swept

    @staticmethod
    def get_sweep_operator_generator(sparse_frame: csc_matrix) -> (
            UnsupervisedSweepOperator, CovarianceGenerator):
        """
        Creates and initializes sweep operator and covariance generator for a sparse frame
        :param sparse_frame: input frame
        :return: sweep_operator, covariance_generator
        """
        rows, cols = sparse_frame.shape
        matrix = CscMatrix(sparse_frame.data, sparse_frame.indices, sparse_frame.indptr, shape=(rows, cols))

        transformations = []
        for _col in range(cols):
            transformations.append(Transformation(0, 0, 0, False))

        blas_service = BlasServiceFactory.get_blas_service()
        generator = CovarianceGenerator(False, matrix, transformations, np.ones(shape=(cols,)), blas_service)
        generator.initialize()
        cov_info = generator.covariance_info

        sweep_operator = UnsupervisedSweepOperator(cov_info.correlation_matrix, blas_service)
        generator.compute_variances()

        return sweep_operator, generator

    def split_bins(self, vector: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Splits a vector to bins with equal frequency.
        :param vector: input vector
        :return: sparse matrix
        """
        bin_count = self.__bin_count
        v_sorted_args = np.argsort(vector)
        elem_count = len(vector)
        dense = np.zeros(shape=(vector.shape[0], bin_count), dtype=vector.dtype)
        for i in range(bin_count):
            start = i * elem_count // (bin_count + 1)
            end = (i + 1) * elem_count // (bin_count + 1)
            dense[v_sorted_args[start:end], i] = 1
        ret_mtx = csc_matrix(dense)
        return ret_mtx.indices, ret_mtx.indptr

    def get_sparse_frame(self) -> Tuple[csc_matrix, List[str]]:
        """
        Gets binned sparse array from data_frame
        In order to concatenate sparse matrices fast. I used 3 array structure of csc matrix.
        :return: sparse matrix
        """
        arbitrary_column = next(iter(self.__frame.values()))
        bin_count = self.__bin_count

        n_r = len(arbitrary_column)
        n_c = len(self.__frame)

        nnz = n_r * n_c

        data = np.ones(shape=(nnz,), dtype=arbitrary_column.dtype)
        row_ptr = np.empty_like(data)
        col_ptr = np.zeros(shape=(n_c * bin_count + 1,), dtype=np.longlong)

        index_to_names = [''] * n_c

        row_start = 0
        index = 0
        for name, column in self.__frame.items():
            if np.isnan(column).all():
                continue
            row_ptr_vec, col_ptr_vec = self.split_bins(column)
            row_end = row_start + row_ptr_vec.shape[0]
            row_ptr[row_start:row_end] = row_ptr_vec
            row_start = row_end
            col_ptr[1 + index * bin_count:1 + (index + 1) * bin_count] = col_ptr[index * bin_count] + col_ptr_vec[1:]
            index_to_names[index] = name
            # print([np.sum(sparse_matrix[:, i]) for i in range(sparse_matrix.shape[1])])
            # del data_frame[name]
            index += 1
        if index == 0:
            return None, None
        nnz = col_ptr[index * bin_count]
        return (csc_matrix((data[:nnz], row_ptr[:nnz], col_ptr[:1 + index * bin_count]),
                           shape=(n_r, index * bin_count)), index_to_names[:index])
