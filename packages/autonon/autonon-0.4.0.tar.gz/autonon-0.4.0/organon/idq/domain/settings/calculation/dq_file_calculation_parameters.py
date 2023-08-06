"""Includes DqFileCalculationParameters class."""
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.input_source.dq_file_input_source_settings import DqFileInputSourceSettings


class DqFileCalculationParameters(DqBaseCalculationParameters[DqFileInputSourceSettings]):
    """DQ calculation parameters for file source type"""
