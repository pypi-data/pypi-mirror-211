"""Includes SamplingSettings class."""
from dataclasses import dataclass
from typing import List

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.sampling.settings.enums.sampling_strategy import SamplingStrategy


@dataclass
class SamplingSettings:
    """Settings for Sampling service"""
    data: pd.DataFrame
    target_column_name: str
    target_type: TargetType
    strata_columns: List[str]
    split_test_data: bool
    test_split_ratio: float
    sampling_strategy: SamplingStrategy
    sampling_ratio: float
    data_sample_ratio: float = None
