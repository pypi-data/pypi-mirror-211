"""
This module includes TransactionFileStats class.
"""
from typing import Dict

import numpy as np

from organon.fl.core.businessobjects.histogram_16 import Histogram16


class TransactionFileStats:
    """
    Statistic details for TransactionFile
    """

    def __init__(self):
        self.__histograms: Dict[str, Histogram16[str]] = {}  # pylint: disable=unsubscriptable-object

    def get_histogram(self, dimension_column_name: str) -> Histogram16:
        """Returns histogram corresponding to given dimension column"""
        return self.__histograms[dimension_column_name]

    def build_indices(self, compression_ratio: float, max_cardinality: int):
        """build indices for each histogram"""
        for histogram in self.__histograms.values():
            histogram.build_indices_with_params(compression_ratio, max_cardinality)

    def add(self, dimension_column_name: str):
        """Adds a new histogram corresponding to given dimension column"""
        if dimension_column_name not in self.__histograms:
            self.__histograms[dimension_column_name] = Histogram16()

    def increment(self, dimension_column_name: str, column_value: str, frequency: np.int64 = None):
        """add a value to column data"""
        self.__histograms[dimension_column_name].add(column_value, frequency)

    def get_index(self, column: str, column_value: str) -> np.short:
        """return index for a column value"""
        return self.__histograms[column].get_index_value(column_value)
