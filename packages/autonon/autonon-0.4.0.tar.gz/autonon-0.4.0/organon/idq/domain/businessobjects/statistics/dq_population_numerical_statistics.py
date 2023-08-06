"""Includes class DqPopulationNumericalStatistics."""
from typing import List

from organon.fl.core.collections.sorted_dict import SortedDict
from organon.idq.domain.businessobjects.statistics.dq_base_statistics import DqBaseStatistics


class DqPopulationNumericalStatistics(DqBaseStatistics):
    """Data class storing dq population numerical statistics."""

    def __init__(self):
        super().__init__()
        self.missing_values: List[float] = None
        self.missing_values_frequencies: SortedDict[float, int] = None
        self.mean: float = None
        self.std_dev: float = None
        self.variance: float = None
        self.min: float = None
        self.max: float = None
        self.max_cardinality: float = None
        self.max_percentage: float = None
        self.min_cardinality: float = None
        self.min_percentage: float = None
