"""Includes CFSSelectionSettings class."""
import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.settings.base_supervised_feature_selection_settings import \
    BaseSupervisedFeatureSelectionSettings


class CFSSelectionSettings(BaseSupervisedFeatureSelectionSettings):
    """Settings for CFS selection service"""

    def __init__(self, data: pd.DataFrame, target: pd.DataFrame, target_type: TargetType, max_backtracks=5,
                 prioritize_performance=False):
        super().__init__(data, target, target_type)
        self.max_backtracks = max_backtracks
        self.prioritize_performance = prioritize_performance
