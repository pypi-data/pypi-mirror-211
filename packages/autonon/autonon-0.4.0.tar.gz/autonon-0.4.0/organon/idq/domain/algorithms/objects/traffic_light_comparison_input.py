"""Includes TrafficLightComparisonInput class."""
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.algorithms.objects.base_comparison_input import BaseComparisonInput


class TrafficLightComparisonInput(BaseComparisonInput):
    """Input dto for traffic light comparisons"""

    def __init__(self):
        super().__init__()
        self.green_threshold: float = None
        self.yellow_threshold: float = None
        self.result_code: DqComparisonResultCode = None
        self.property_code: str = None
        self.message: str = None
