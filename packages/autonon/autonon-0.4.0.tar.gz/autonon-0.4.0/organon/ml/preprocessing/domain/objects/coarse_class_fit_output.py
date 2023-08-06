"""Includes CoarseClassFitOutput class"""
from typing import List, Union

import pandas as pd


class CoarseClassFitOutput:
    """Output of CoarseClass fitting process."""

    def __init__(self):
        self.target_mean: Union[float, int] = None
        self.char_table: pd.DataFrame = None
        self.coarse_class_table: pd.DataFrame = None
        self.rejected_list: List[str] = None
