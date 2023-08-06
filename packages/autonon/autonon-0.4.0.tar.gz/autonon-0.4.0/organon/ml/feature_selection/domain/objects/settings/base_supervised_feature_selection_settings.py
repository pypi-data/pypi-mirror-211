"""Includes BaseSupervisedFeatureSelectionSettings class."""
import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.settings.base_feature_selection_settings import \
    BaseFeatureSelectionSettings


class BaseSupervisedFeatureSelectionSettings(BaseFeatureSelectionSettings):
    """Base settings for supervised feature selection services"""

    def __init__(self, data: pd.DataFrame, target: pd.DataFrame, target_type: TargetType):
        super().__init__(data)
        self.target: pd.DataFrame = target
        self.target_type: TargetType = target_type
