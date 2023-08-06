"""Includes DqControlParameters class."""
from typing import List, Dict

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_test_group import DqTestGroup
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.abstractions.dq_base_comparison_parameters import DqBaseComparisonParameters
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo


class DqControlParameters:
    """Parameters for DqControl execution"""

    def __init__(self):
        self.comparison_parameters: DqBaseComparisonParameters = None
        self.control_parameters: List[DqBaseCalculationParameters] = None
        self.control_results: List[DqCalculationResult] = None
        self.test_calc_parameters: DqBaseCalculationParameters = None
        self.test_calc_result: DqCalculationResult = None
        self.test_group_info: Dict[DqTestGroupType, DqTestGroup] = None

    def get_comparison_cols_by_native_type(self, col_native_type: ColumnNativeType) -> List[DqComparisonColumnInfo]:
        """Returns comparison column info for columns of given native type"""
        comparison_cols = self.comparison_parameters.comparison_columns
        data_col_collection = self.test_calc_result.data_source_stats.data_column_collection
        col_names = [col.column_name for col in data_col_collection if col.column_native_type == col_native_type]
        return [col for col in comparison_cols if col.column_name in col_names]

    def get_nominal_comparison_columns(self) -> List[DqComparisonColumnInfo]:
        """Returns nominal comparison columns"""
        nominal_columns = []
        for col_type in self.test_calc_parameters.nominal_column_types:
            nominal_columns.extend(self.get_comparison_cols_by_native_type(col_type))
        return nominal_columns
