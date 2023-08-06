"""Includes HighCorrReductionOutput class"""
from typing import Dict

from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput


class HighCorrReductionOutput(FeatureReductionOutput):
    """Output of high correlation feature reduction"""

    def __init__(self):
        super().__init__()
        self.new_univariate_performance_results: Dict[str, float] = None
