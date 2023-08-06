"""Includes DqSampleNumericalStatistics class."""
from typing import List

from organon.fl.core.collections.sorted_dict import SortedDict
from organon.fl.mathematics.businessobjects.sets.interval import Interval
from organon.fl.mathematics.businessobjects.sets.sum_triple import SumTriple
from organon.idq.domain.businessobjects.statistics.dq_base_statistics import DqBaseStatistics
from organon.idq.domain.helpers.statistics.dq_statistical_functions import DqStatisticalFunctions


class DqSampleNumericalStatistics(DqBaseStatistics):
    """todo"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        super().__init__()
        self.missing_values: List[float] = None
        self.missing_values_frequencies: SortedDict[float, int] = None
        self.compute_frequencies: bool = None
        self.frequencies: SortedDict[float, float] = None
        self.interval_statistics: SortedDict[Interval, SumTriple] = None
        self.mean: float = None
        self.trimmed_mean: float = None
        self.std_dev: float = None
        self.variance: float = None
        self.min: float = None
        self.max: float = None
        self.sum: float = None
        self.median: float = None
        self.inter_quartile_range: float = None
        self.tukey_lower_limit: float = None
        self.tukey_upper_limit: float = None
        self.percentile_values: SortedDict[int, float] = None
        self.quartile_values: SortedDict[int, float] = None

    @property
    def percentages(self):
        """todo"""
        return DqStatisticalFunctions.get_percentages_from_frequencies_for_sorted(self.frequencies)

    @staticmethod
    def get_null_statistics():
        """Return DqSampleNumericalStatistics with null statistics."""
        stats = DqSampleNumericalStatistics()
        stats.n_val = 0
        stats.n_miss = 0
        stats.cardinality = 0
        stats.compute_frequencies = False
        stats.mean = float("nan")
        stats.trimmed_mean = float("nan")
        stats.std_dev = float("nan")
        stats.variance = float("nan")
        stats.min = float("nan")
        stats.max = float("nan")
        stats.sum = float("nan")
        stats.median = float("nan")
        stats.inter_quartile_range = float("nan")
        stats.tukey_lower_limit = float("nan")
        stats.tukey_upper_limit = float("nan")
        return stats
