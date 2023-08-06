"""Module for LinearRegressionParameter"""
from dataclasses import dataclass


@dataclass
class LinearRegressionParameter:
    """Statistical info for swept parameters"""
    estimate: float
    standard_error: float
    test_statistic: float
    p_value: float
    vif: float
    standardized_coefficient: float
    lower_confidence_limit: float
    upper_confidence_limit: float
