"""Includes DqDataSource class"""
from typing import Optional

import pandas as pd


class DqDataSource:
    """DqDataSource attributes"""

    def __init__(self):
        self.sampled_data: Optional[pd.DataFrame] = None
        self.full_data_row_count: int = None
