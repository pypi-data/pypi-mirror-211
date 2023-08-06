"""Includes BaseFeatureSelecter class."""
import abc

import pandas as pd


class BaseFeatureSelecter(metaclass=abc.ABCMeta):
    """Base user service for feature selection"""

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def run(self):
        """Run selecter and return output"""
        return self._run()

    @abc.abstractmethod
    def _run(self):
        raise NotImplementedError
