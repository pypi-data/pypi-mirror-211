"""Includes TrafficLightComparisonInput class."""
from organon.idq.core.enums.dq_comparison_result_code import DqComparisonResultCode
from organon.idq.domain.algorithms.objects.base_comparison_input import BaseComparisonInput


class TimeSeriesComparisonInput(BaseComparisonInput):
    """Input dto for time series comparisons"""

    def __init__(self):
        super().__init__()
        self.z_score: float = None
        self.green_threshold: float = None
        self.yellow_threshold: float = None
        self.ci_code: DqComparisonResultCode = None
        self.tl_code: DqComparisonResultCode = None
        self.ad_code: DqComparisonResultCode = None
        self.ci_message: str = None
        self.tl_message: str = None
        self.ad_message: str = None
