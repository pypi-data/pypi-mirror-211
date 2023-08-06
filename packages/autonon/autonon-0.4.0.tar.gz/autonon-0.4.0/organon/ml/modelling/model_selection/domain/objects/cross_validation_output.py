"""Includes CrossValidationOutput class"""
from typing import List

import numpy as np

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller


class CrossValidationOutput:
    """Output of CrossValidation"""

    def __init__(self):
        self.fold_scores: List[List[float]] = None
        self.mean_scores: List[float] = None
        self.best_modeller: BaseModeller = None
        self.test_fold: np.ndarray = None
