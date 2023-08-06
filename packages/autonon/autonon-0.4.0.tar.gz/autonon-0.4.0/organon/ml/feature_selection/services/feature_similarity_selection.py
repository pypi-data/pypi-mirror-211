"""Includes FeatureSimilaritySelection class"""
from typing import Optional

import pandas as pd

from organon.ml.feature_selection.domain.objects.feature_similarity_selection_output import \
    FeatureSimilaritySelectionOutput
from organon.ml.feature_selection.domain.objects.settings.feature_similarity_selection_settings import \
    FeatureSimilaritySelectionSettings
from organon.ml.feature_selection.domain.services.feature_similarity_selection_service import \
    FeatureSimilaritySelectionService
from organon.ml.feature_selection.services.abstractions.base_unsupervised_feature_selecter import \
    BaseUnsupervisedFeatureSelecter


class FeatureSimilaritySelection(BaseUnsupervisedFeatureSelecter):
    """Feature selecter which utilizes a feature similarity algorithm for selection"""

    def __init__(self, data: pd.DataFrame, *, selection_percent: float = 0.05,
                 prioritize_performance: bool = False):
        super().__init__(data)
        self.settings = FeatureSimilaritySelectionSettings(data, selection_percent=selection_percent,
                                                           prioritize_performance=prioritize_performance)
        self.output: Optional[FeatureSimilaritySelectionOutput] = None

    def _run(self):
        service = FeatureSimilaritySelectionService()
        self.output = service.run_selection(self.settings)
        return self.output
