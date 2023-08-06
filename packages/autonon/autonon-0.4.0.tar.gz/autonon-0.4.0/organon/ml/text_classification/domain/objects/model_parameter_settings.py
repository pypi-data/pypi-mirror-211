"""Includes ModelParameterSettings Class"""
from typing import List


class ModelParameterSettings:
    """Class for model parameters"""

    def __init__(self, batch_size: int = 10, epochs: int = 20, metrics: List[str] = None):
        self.batch_size: int = batch_size
        self.epochs: int = epochs
        self.metrics: List[str] = metrics
