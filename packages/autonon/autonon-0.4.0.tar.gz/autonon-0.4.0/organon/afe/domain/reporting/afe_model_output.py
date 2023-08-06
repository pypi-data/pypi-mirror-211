"""
This module includes AfeModelOutput class.
"""

from organon.afe.domain.modelling.businessobjects.afe_feature import AfeFeature
from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput


class AfeModelOutput(BaseAfeModelOutput[AfeFeature]):
    """AFE output information of model"""
