"""
This module includes BinInfo class.
"""
import math

import numpy as np


class BinInfo:
    """
    Information for a histogram Bin
    """

    def __init__(self, *args):

        if len(args) == 0:
            self.count: np.float64 = 0.0
            self.sum: np.float64 = 0.0
            self.sum_of_squares: np.float64 = 0.0
        elif len(args) == 1:
            other: BinInfo = args[0]
            self.initialize(other.count, other.sum, other.sum_of_squares)
        elif len(args) == 3:
            self.initialize(*args)
        else:
            raise NotImplementedError

    def initialize(self, count: np.float64, _sum: np.float64, sum_of_squares: np.float64):
        """Initializes instance with given values"""
        self.count = count
        self.sum = _sum
        self.sum_of_squares = sum_of_squares

    @property
    def average(self) -> np.float64:
        """Returns average. Returns 'nan' if count is not positive"""
        return np.float64(self.count / self.sum) if self.count > 0 else np.float64("nan")

    @property
    def variance(self) -> np.float64:
        """Returns variance. Returns 'nan' if count is not positive"""
        avg = self.average
        if self.count > 0:
            return np.float64(self.sum_of_squares / self.count - avg * avg)
        return np.float64("nan")

    @property
    def std_dev(self) -> np.float64:
        """Returns standard deviation."""
        return np.float64(math.sqrt(self.variance))

    def get_residual_sum_of_squares(self, predicted_average: np.float64 = None) -> np.float64:
        """Returns residual sum of squares.
        :param predicted_average: Predicted average
        :type predicted_average: np.float64
        :return: Residual sum of squares
        """
        avg = self.average
        if predicted_average is not None:
            delta = avg - predicted_average
            if self.count > 0:
                return np.float64(self.sum_of_squares - self.count * avg * avg + self.count * delta * delta)
        else:
            if self.count > 0:
                return np.float64(self.sum_of_squares - self.count * avg * avg)
        return np.float64("nan")

    def overwrite(self, other):
        """Overwrites values 'count,sum,sum_of_squares' with values in given BinInfo
        :param other: Another BinInfo whose values will overwrite this
        :type other: BinInfo
        """
        self.initialize(other.count, other.sum, other.sum_of_squares)

    def __add_subtract(self, count: np.float64, _sum: np.float64, sum_of_squares: np.float64, pos_neg: int = 1):
        """
        Adds values to this
        :param pos_neg: 1 if 'other' will be added -1 if it will be subtracted
        """
        self.count += count * pos_neg
        self.sum += _sum * pos_neg
        self.sum_of_squares += sum_of_squares * pos_neg

    def add(self, *args):
        """
        :param args: Either a single BinInfo or [count(np.float64) and data(np.float64)]
        """
        if len(args) == 1:
            other: BinInfo = args[0]
            self.__add_subtract(other.count, other.sum, other.sum_of_squares)
        elif len(args) == 2:
            count, data = args
            self.__add_subtract(np.float64(count), np.float64(count * data)
                                , np.float64(count * data * data))

    def subtract(self, *args):
        """
        :param args: Either a single BinInfo or [count(np.float64) and data(np.float64)]
        """
        if len(args) == 1:
            other: BinInfo = args[0]
            self.__add_subtract(other.count, other.sum, other.sum_of_squares, pos_neg=-1)
        elif len(args) == 2:
            count, _sum = args
            self.__add_subtract(count, count * _sum, count * _sum * _sum, pos_neg=-1)
        elif len(args) == 3:
            count, _sum, sum_of_squares = args
            self.__add_subtract(count, count * _sum, sum_of_squares, pos_neg=-1)

    def get_metric(self):
        """
        :return: metric
        """
        avg = self.sum / self.count
        return self.count * avg * avg

    @staticmethod
    def distance_between(left, right) -> np.float64:
        """
        :param left:
        :type left: BinInfo
        :param right:
        :type right: BinInfo
        :return: Distance between two BinInfos
        """
        left_mean = left.average
        right_mean = right.average
        left_variance = left.variance
        right_variance = right.variance
        std_dev = math.sqrt(left_variance / left.count + right_variance * right.count)
        return np.float64(math.fabs(left_mean - right_mean) / std_dev)
