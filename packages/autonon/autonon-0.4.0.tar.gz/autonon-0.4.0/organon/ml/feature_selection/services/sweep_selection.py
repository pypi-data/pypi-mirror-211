"""Includes SweepSelection class."""
from typing import Optional

import pandas as pd

from organon.ml.feature_selection.domain.objects.settings.sweep_selection_settings import SweepSelectionSettings
from organon.ml.feature_selection.domain.objects.sweep_selection_output import SweepSelectionOutput
from organon.ml.feature_selection.domain.services.sweep_selection_service import SweepSelectionService
from organon.ml.feature_selection.services.abstractions.base_unsupervised_feature_selecter import \
    BaseUnsupervisedFeatureSelecter


class SweepSelection(BaseUnsupervisedFeatureSelecter):
    """Feature selecter which utilizes sweep algorithm for selection"""

    def __init__(self, data: pd.DataFrame, *, bin_count: int = None, r_factor: float = None, random_state: int = None,
                 max_col_count: int = None, n_threads: int = 1):
        super().__init__(data)
        self.settings = SweepSelectionSettings(data, bin_count=bin_count, r_factor=r_factor, random_state=random_state,
                                               max_col_count=max_col_count, n_threads=n_threads)
        self.output: Optional[SweepSelectionOutput] = None

    def _run(self):
        service = SweepSelectionService()
        self.output = service.run_selection(self.settings)
        return self.output
