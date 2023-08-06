"""Includes ISampleDataService interface"""
import abc

import pandas as pd


class ISampleDataService(metaclass=abc.ABCMeta):
    """Interface for SampleData services."""

    @abc.abstractmethod
    def get_sample(self) -> pd.DataFrame:
        """Read and return sample as pd.DataFrame"""
