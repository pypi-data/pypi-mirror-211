"""Includes SamplingOutput class."""
import pandas as pd


class SamplingOutput:
    """Output of Sampling service"""

    def __init__(self):
        self.train_data: pd.DataFrame = None
        self.test_data: pd.DataFrame = None
