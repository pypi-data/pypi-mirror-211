"""Includes BaseFeatureSelectionSettings class."""
import pandas as pd


class BaseFeatureSelectionSettings:
    """Base settings for all feature selection services"""
    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data
