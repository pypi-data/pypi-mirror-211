"""Includes DqDbFullProcessInput class."""
from organon.idq.domain.settings.abstractions.dq_full_process_input import DqFullProcessInput
from organon.idq.domain.settings.calculation.dq_df_calculation_parameters import DqDfCalculationParameters
from organon.idq.domain.settings.comparison.dq_df_comparison_parameters import DqDfComparisonParameters


class DqDfFullProcessInput(DqFullProcessInput[DqDfCalculationParameters, DqDfComparisonParameters]):
    """DQ comparison parameters for pandas dataframe source type"""
