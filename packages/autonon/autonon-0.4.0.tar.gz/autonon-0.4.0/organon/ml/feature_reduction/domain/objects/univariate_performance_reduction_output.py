"""Includes UnivariatePerformanceFeatureReductionOutput class"""
from typing import Dict

from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput


class UnivariatePerformanceFeatureReductionOutput(FeatureReductionOutput):
    """Output of univariate performance feature reduction"""

    def __init__(self):
        super().__init__()
        self.univariate_performance_result: Dict[str, float] = None
