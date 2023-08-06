"""todo"""
from typing import List

from organon.idq.domain.businessobjects.dq_calculation_result import DqCalculationResult
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo


class PsiComparer:
    """todo"""

    @staticmethod
    def nominal_columns_psi_comparer(controls: List[DqCalculationResult],
                                     t_calc_result: DqCalculationResult,
                                     test_nominal_cols: List[DqComparisonColumnInfo],
                                     bmh: int, psi_yellow: float, psi_red: float) -> List[DqComparisonResult]:
        """todo"""

    @staticmethod
    def numerical_columns_psi_comparer(controls: List[DqCalculationResult],
                                       t_calc_result: DqCalculationResult,
                                       test_nominal_cols: List[DqComparisonColumnInfo],
                                       bmh: int, psi_yellow: float, psi_red: float) -> List[DqComparisonResult]:
        """todo"""
        # frame = t_calc_result.sample_data  # c# taki frame argümanı yerine
