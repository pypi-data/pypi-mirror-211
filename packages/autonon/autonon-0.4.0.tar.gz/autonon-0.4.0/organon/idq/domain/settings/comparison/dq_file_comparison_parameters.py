"""Includes DqFileComparisonParameters class."""
from organon.idq.domain.settings.abstractions.dq_base_comparison_parameters import DqBaseComparisonParameters
from organon.idq.domain.settings.input_source.dq_file_input_source_settings import DqFileInputSourceSettings


class DqFileComparisonParameters(DqBaseComparisonParameters[DqFileInputSourceSettings]):
    """DQ comparison parameters for file source type"""
