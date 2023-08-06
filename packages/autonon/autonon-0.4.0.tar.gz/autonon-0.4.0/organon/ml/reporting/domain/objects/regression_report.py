"""Includes RegressionReport class."""

import pandas as pd

from organon.ml.reporting.domain.objects.base_report import BaseReport


class RegressionReport(BaseReport):
    """Report for regression"""

    def __init__(self):
        self.performance_summary: pd.DataFrame = None
        self.lift_table: pd.DataFrame = None
