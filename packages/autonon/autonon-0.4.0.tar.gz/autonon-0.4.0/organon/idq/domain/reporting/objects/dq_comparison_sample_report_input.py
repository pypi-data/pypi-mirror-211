"""Includes DqComparisonReportInput class"""
from typing import List

from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.businessobjects.dq_data_column_collection import DqDataColumnCollection
from organon.idq.domain.reporting.objects.base_alert_info import BaseAlertInfo
from organon.idq.domain.reporting.objects.nominal_column_control_details import NominalColumnControlDetails
from organon.idq.domain.reporting.objects.numeric_column_control_details import NumericColumnControlDetails
from organon.idq.domain.reporting.objects.table_control_details import TableControlDetails


class DqComparisonSampleReportInput:
    """Class for DqComparisonSampleReportInput"""

    def __init__(self):
        self.dq_data_column_collection: DqDataColumnCollection = None
        self.dq_comparison_result: List[DqComparisonResult] = None
        self.alert_info: List[BaseAlertInfo] = None
        self.numeric_columns_control: List[NumericColumnControlDetails] = None
        self.nominal_columns_control: List[NominalColumnControlDetails] = None
        self.table_control: List[TableControlDetails] = None
