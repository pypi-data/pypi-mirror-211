"""Includes SelectionSettings class."""
from dataclasses import dataclass
from typing import List

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller


@dataclass
class SelectionSettings:
    """Settings for model selection"""
    modellers: List[BaseModeller]
    train_data: pd.DataFrame
    target_data: pd.Series
    target_type: TargetType
    cv_count: int = None
    test_data: pd.DataFrame = None
    test_target_data: pd.Series = None
    add_stacking: bool = True
    add_voting: bool = True
    num_threads_for_parallel_fit: int = None
    num_threads_for_parallel_cv: int = None
