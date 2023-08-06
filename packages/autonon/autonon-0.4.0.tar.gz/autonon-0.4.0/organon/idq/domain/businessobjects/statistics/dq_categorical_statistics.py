"""Includes DqCategoricalStatistics class"""

from typing import List, Dict

from organon.idq.domain.businessobjects.statistics.dq_base_statistics import DqBaseStatistics
from organon.idq.domain.helpers.statistics.dq_statistical_functions import DqStatisticalFunctions


class DqCategoricalStatistics(DqBaseStatistics):
    """todo"""

    def __init__(self, missing_values: List[object], frequencies: Dict[object, float] = None):
        super().__init__()
        if frequencies is None:
            frequencies = {}
        self.missing_values: List[object] = missing_values
        self.frequencies: Dict[object, float] = frequencies
        self.cardinality = 0
        self.n_miss = 0
        self.n_val = 0

    @property
    def percentages(self) -> Dict[object, float]:
        """todo"""
        return DqStatisticalFunctions.get_percentages_from_frequencies(self.frequencies)

    def add(self, key: object, frequency: float):
        """Adds frequency value to statistics"""
        if key in self.frequencies:
            self.frequencies[key] += frequency
        else:
            self.frequencies[key] = frequency
            if key not in self.missing_values:
                self.cardinality += 1
        if key in self.missing_values:
            self.n_miss += frequency
        self.n_val += frequency
