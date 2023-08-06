"""Includes SourceWithDateDqOutputReport class."""
import pandas as pd
from organon.idq.domain.reporting.objects.base_dq_output_report import BaseDqOutputReport


class SourceWithPartitionsDqOutputReport(BaseDqOutputReport):
    """Output report for DQ execution."""

    def __init__(self):
        super().__init__()
        self.table_control_details_df: pd.DataFrame = None
        self.numeric_column_control_details_df: pd.DataFrame = None
        self.nominal_column_control_details_df: pd.DataFrame = None
