"""Module for LinearRegressionAlgorithmSettings"""
from dataclasses import dataclass
import numpy as np

from organon.fl.mathematics.sweep.enums import RegressionAttributeSelectionMethod


@dataclass
class LinearRegressionAlgorithmSettings:
    """Settings for the Linear Regression"""
    target: int
    weight: np.ndarray
    attribute_selection_method: RegressionAttributeSelectionMethod
    inclusion_confidence_level: float
    exclusion_confidence_level: float
    inclusion_f_statistics: float
    exclusion_f_statistics: float
    use_positive_coefficients: bool
    use_intercept: bool
    min_r_squared_change_in_train_set: float
    min_r_squared_change_in_validation_set: float
    maximum_vif: float
    tolerance: float
