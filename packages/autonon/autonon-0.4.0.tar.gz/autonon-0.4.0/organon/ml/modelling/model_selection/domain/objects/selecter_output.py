"""Includes SelecterOutput class"""
from typing import List

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller


class SelecterOutput:
    """Output of Selecter"""

    def __init__(self):
        self.best_modeller: BaseModeller = None
        self.modeller_fold_scores: List[List[float]] = None
        self.modeller_scores: List[float] = None
        self.stacking_fold_scores: List[float] = None
        self.stacking_score: float = None
        self.voting_fold_scores: List[float] = None
        self.voting_score: float = None
