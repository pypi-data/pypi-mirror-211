"""Includes DqDfCalculationParameters class."""

from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.input_source.dq_df_input_source_settings import DqDfInputSourceSettings


class DqDfCalculationParameters(DqBaseCalculationParameters[DqDfInputSourceSettings]):
    """DQ calculation parameters for dataframe source type"""
