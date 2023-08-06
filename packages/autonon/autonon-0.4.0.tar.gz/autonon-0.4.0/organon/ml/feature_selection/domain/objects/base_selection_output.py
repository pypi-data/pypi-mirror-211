"""Includes BaseSelectionOutput class."""
from typing import List


class BaseSelectionOutput:
    """Base output for feature selection services"""
    def __init__(self):
        self.selected_features: List[str] = None
