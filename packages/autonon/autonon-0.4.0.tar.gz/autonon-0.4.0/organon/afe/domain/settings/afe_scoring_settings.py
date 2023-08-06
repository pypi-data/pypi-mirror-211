"""
This module includes AfeScoringSettings class.
"""

from organon.afe.domain.reporting.afe_model_output import AfeModelOutput
from organon.afe.domain.settings.base_afe_scoring_settings import BaseAfeScoringSettings


class AfeScoringSettings(BaseAfeScoringSettings[AfeModelOutput]):
    """
    Scoring settings for AFE
    """
    ATTR_DICT = {
        "model_output": AfeModelOutput
    }
    ATTR_DICT.update(BaseAfeScoringSettings.ATTR_DICT)
