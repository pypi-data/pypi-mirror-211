"""Includes DqFileFullProcessInput class."""
from organon.idq.domain.settings.abstractions.dq_full_process_input import DqFullProcessInput
from organon.idq.domain.settings.calculation.dq_file_calculation_parameters import DqFileCalculationParameters
from organon.idq.domain.settings.comparison.dq_file_comparison_parameters import DqFileComparisonParameters


class DqFileFullProcessInput(DqFullProcessInput[DqFileCalculationParameters, DqFileComparisonParameters]):
    """DQ comparison parameters for text file source type"""
