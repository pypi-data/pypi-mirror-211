"""Includes DqComparisonParameters class."""
from typing import TypeVar, Generic, List

from organon.idq.domain.businessobjects.dq_test_group import DqTestGroup
from organon.idq.domain.settings.abstractions.dq_base_input_source_settings import DqBaseInputSourceSettings
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo

T = TypeVar("T", bound=DqBaseInputSourceSettings)


class DqBaseComparisonParameters(Generic[T]):
    """Dq comparison settings"""

    def __init__(self):
        self.comparison_columns: List[DqComparisonColumnInfo] = None
        self.maximum_nom_cardinality: int = None
        self.minimum_cardinality: int = None
        self.traffic_light_threshold_yellow: float = None
        self.traffic_light_threshold_green: float = None
        self.psi_threshold_yellow: float = None
        self.psi_threshold_green: float = None
        self.z_score: float = None
        self.test_groups: List[DqTestGroup] = None
