"""Includes FeatureSimilaritySelectionSettings class"""
import pandas as pd

from organon.ml.feature_selection.domain.objects.settings.base_unsupervised_feature_selection_settings import \
    BaseUnsupervisedFeatureSelectionSettings


class FeatureSimilaritySelectionSettings(BaseUnsupervisedFeatureSelectionSettings):
    """Settings for feature similarity selection"""

    def __init__(self, data: pd.DataFrame, selection_percent: float = 0.05, prioritize_performance: bool = False):
        super().__init__(data)
        self.selection_percent: float = selection_percent
        self.prioritize_performance = prioritize_performance
