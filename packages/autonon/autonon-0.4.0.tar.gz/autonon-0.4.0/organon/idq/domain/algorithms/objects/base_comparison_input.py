"""Includes BaseComparisonInput class."""
from typing import List

from organon.idq.core.enums.data_entity_type import DataEntityType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType


class BaseComparisonInput:
    """Base input dto for time series ad traffic light comparisons"""

    def __init__(self):
        self.data_entity: DataEntityType = None
        self.data_entity_name: str = None
        self.test_group: DqTestGroupType = None
        self.past_series: List[float] = None
        self.current_value: float = None
