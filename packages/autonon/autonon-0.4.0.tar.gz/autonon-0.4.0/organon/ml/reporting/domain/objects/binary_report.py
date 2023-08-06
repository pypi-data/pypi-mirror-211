"""Includes BinaryReport class."""
import pandas as pd

from organon.ml.reporting.domain.objects.base_report import BaseReport


class BinaryReport(BaseReport):
    """Report for binary classification"""

    def __init__(self):
        self.performance_summary: pd.DataFrame = None
        self.detailed_performance_summary: pd.DataFrame = None
        self.target_based_performance_summary: pd.DataFrame = None
