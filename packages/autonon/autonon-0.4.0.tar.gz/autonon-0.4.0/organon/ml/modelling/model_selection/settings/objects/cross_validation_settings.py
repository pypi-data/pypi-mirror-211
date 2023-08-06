"""Includes CrossValidationSettings class"""
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller


@dataclass
class CrossValidationSettings:
    """Settings for CrossValidation"""
    modellers: List[BaseModeller]
    train_data: pd.DataFrame
    target_data: pd.Series
    cv_count: int
    bin_count: Optional[int]
    return_test_fold: bool
