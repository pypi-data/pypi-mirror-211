"""todo"""
from typing import List

from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo


class ColumnValuesComparer:
    """todo"""

    @staticmethod
    def compare_unexpected_nominal_values(controls: List[DqCalculationResult],
                                          t_calc_result: DqCalculationResult,
                                          test_nominal_cols: List[DqComparisonColumnInfo], bmh: int) \
            -> List[DqComparisonResult]:
        """todo"""

    @staticmethod
    def compare_unexpected_numerical_values(controls: List[DqCalculationResult],
                                            t_calc_result: DqCalculationResult,
                                            test_numerical_cols: List[DqComparisonColumnInfo], bmh: int) \
            -> List[DqComparisonResult]:
        """todo"""

    @staticmethod
    def test_nominal_column_values(t_calc_result: DqCalculationResult,
                                   nominal_columns_collection: List[DqComparisonColumnInfo],
                                   minimum_cardinality: int) -> List[DqComparisonResult]:
        """todo"""

    @staticmethod
    def test_numerical_column_values(t_calc_result: DqCalculationResult,
                                     numerical_columns_collection: List[DqComparisonColumnInfo],
                                     minimum_cardinality: int) -> List[DqComparisonResult]:
        """todo"""
