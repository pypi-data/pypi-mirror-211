"""
This module includes AfeOutputReport class.
"""

from organon.afe.domain.modelling.businessobjects.afe_feature import AfeFeature
from organon.afe.domain.reporting.base_afe_output_report import BaseAfeOutputReport


class AfeOutputReport(BaseAfeOutputReport[AfeFeature]):
    """Afe output information to be reported."""
