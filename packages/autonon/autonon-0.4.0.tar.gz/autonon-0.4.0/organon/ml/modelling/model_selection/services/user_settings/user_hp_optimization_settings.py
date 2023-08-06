"""Includes UserHPOptimizationSettings class."""
from dataclasses import dataclass
from typing import List, Dict, Optional

import pandas as pd


@dataclass
class UserHPOptimizationSettings:
    """User settings class for HPOptimizer"""
    train_data: pd.DataFrame
    target_data: pd.Series
    search_method: str
    modellers: List[str] = None
    modeller_params: List[Dict[str, list]] = None
    cv_fold: int = None
    scoring_metrics: Optional[List[str]] = None
    test_data: pd.DataFrame = None
    test_target_data: pd.Series = None
    search_params: dict = None
