"""todo"""
from typing import Optional, Dict

from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import DqCategoricalStatistics
from organon.idq.domain.businessobjects.statistics.dq_population_numerical_statistics import \
    DqPopulationNumericalStatistics


class PopulationStatistics:
    """todo"""
    def __init__(self):
        self.nominal_statistics: Optional[Dict[str, DqCategoricalStatistics]] = None
        self.numerical_statistics: Optional[Dict[str, DqPopulationNumericalStatistics]] = None
