"""Includes SweepSelectionSettings class"""
import pandas as pd

from organon.ml.feature_selection.domain.objects.settings.base_unsupervised_feature_selection_settings import \
    BaseUnsupervisedFeatureSelectionSettings


class SweepSelectionSettings(BaseUnsupervisedFeatureSelectionSettings):
    """Settings for sweep selection"""

    def __init__(self, data: pd.DataFrame, bin_count: int = None, r_factor: float = None, random_state: int = None,
                 max_col_count: int = None, n_threads: int = 1):
        super().__init__(data)
        self.bin_count = bin_count
        self.r_factor = r_factor
        self.random_state = random_state
        self.max_col_count = max_col_count
        self.n_threads = n_threads
