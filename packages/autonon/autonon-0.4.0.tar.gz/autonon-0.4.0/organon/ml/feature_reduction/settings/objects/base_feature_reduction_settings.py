"""Includes FeatureReductionSettings class."""
from typing import List, Optional
from pandas import DataFrame


class BaseFeatureReductionSettings:
    """Settings for base feature reduction"""
    def __init__(self, data: DataFrame, excluded_columns: Optional[List[str]] = None):
        self.data = data
        self.excluded_columns = excluded_columns
