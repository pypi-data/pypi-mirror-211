"""Includes UserSelectionSettings class"""
from dataclasses import dataclass
from typing import List

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller


@dataclass
class UserSelectionSettings:
    """Settings entered by user for Selecter"""
    modellers: List[BaseModeller]
    train_data: pd.DataFrame
    target_data: pd.Series
    target_type: str
    cv_count: int
    test_data: pd.DataFrame
    test_target_data: pd.Series
    add_stacking: bool
    add_voting: bool
    num_threads_for_parallel_fit: int = None
    num_threads_for_parallel_cv: int = None
