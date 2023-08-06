"""Includes UserSamplingSettings class"""
from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class UserSamplingSettings:
    """Stores sampling settings entered by user"""
    data: pd.DataFrame
    target_column_name: str
    target_type: str
    strata_columns: List[str]
    split_test_data: bool
    test_split_ratio: float
    sampling_strategy: str
    sampling_ratio: float
    data_sample_ratio: float
