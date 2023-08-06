"""Includes HPOptimizationSettings class"""
from dataclasses import dataclass
from typing import List, Dict, Optional

import pandas as pd

from organon.ml.modelling.algorithms.core.enums.modeller import Modeller
from organon.ml.modelling.model_selection.settings.enums.search_type import SearchType


@dataclass
class HPOptimizationSettings:
    """Settings for HPOService"""
    train_data: pd.DataFrame
    target_data: pd.Series
    search_method: SearchType
    modellers: List[Modeller] = None
    modeller_params: List[Dict[str, list]] = None
    cv_fold: int = None
    scoring_metrics: Optional[List[str]] = None
    test_data: pd.DataFrame = None
    test_target_data: pd.Series = None
    search_params: dict = None
