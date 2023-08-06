"""Includes DqDfComparisonParameters class."""
from organon.idq.domain.settings.abstractions.dq_base_comparison_parameters import DqBaseComparisonParameters
from organon.idq.domain.settings.input_source.dq_df_input_source_settings import DqDfInputSourceSettings


class DqDfComparisonParameters(DqBaseComparisonParameters[DqDfInputSourceSettings]):
    """DQ comparison parameters for dataframe source type"""
