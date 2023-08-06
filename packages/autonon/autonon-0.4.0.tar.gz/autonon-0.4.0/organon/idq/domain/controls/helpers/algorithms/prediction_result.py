"""This module includes PredictionResult"""
from typing import List


class PredictionResult:
    """Class for PredictionResult"""

    def __init__(self, actual: list):
        self.predictions: List[float] = None
        self.actual: List[float] = actual
        self.mean_square_err: float = None
