"""Includes BaseDqOutputReport class."""
import abc
from typing import List

import pandas as pd

from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection


class BaseDqOutputReport(metaclass=abc.ABCMeta):
    """Output report for DQ execution."""

    def __init__(self):
        self.alerts_df: pd.DataFrame = None
        self.signals_df: pd.DataFrame = None
        self.signals: List[DqComparisonResult] = None
        self.column_collection: DqDataColumnCollection = None
