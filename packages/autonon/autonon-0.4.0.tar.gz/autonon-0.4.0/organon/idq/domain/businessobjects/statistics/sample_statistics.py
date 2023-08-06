"""todo"""
from typing import Dict

from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import \
    DqCategoricalStatistics
from organon.idq.domain.businessobjects.statistics.dq_sample_numerical_statistics import \
    DqSampleNumericalStatistics


class SampleStatistics:
    """todo"""

    def __init__(self):
        self.numerical_statistics: Dict[str, DqSampleNumericalStatistics] = None
        self.nominal_statistics: Dict[str, DqCategoricalStatistics] = None
