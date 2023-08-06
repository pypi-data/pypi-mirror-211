"""This module includes "SumTriple" class."""
import numpy as np


class SumTriple:
    """Class for SumTriple"""

    def __init__(self, count: float = 0.0, sum_: float = 0.0, sum_of_squares: float = 0.0):
        self.count: float = count
        self.sum_: float = sum_
        self.sum_of_squares: float = sum_of_squares

    @property
    def average(self) -> float:
        """Returns average of SumTriple."""
        average = self.sum_ / self.count if self.count > 0 else float('nan')
        return average

    @property
    def variance(self) -> float:
        """Returns variance of SumTriple."""
        average = self.average
        variance = self.sum_of_squares / self.count - average * average if self.count > 0 else float('nan')
        return variance

    @property
    def std_dev(self) -> float:
        """Returns std_dev of SumTriple."""
        return np.sqrt(self.variance)

    def update_with_data(self, count: float, data: float):
        """Update class attribute with data"""
        self.count = self.count + count
        self.sum_ = self.sum_ + count * data
        self.sum_of_squares = self.sum_of_squares + count * data * data

    def update_with_sum_triple(self, triple:"SumTriple"):
        """Update class attribute with SumTriple Object"""
        self.count = self.count + triple.count
        self.sum_ = self.sum_ + triple.sum_
        self.sum_of_squares = self.sum_of_squares + triple.sum_of_squares
