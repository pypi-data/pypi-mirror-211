"""Includes RFSelectionSettings class"""
from typing import Any, Dict, Optional

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.settings.base_supervised_feature_selection_settings import \
    BaseSupervisedFeatureSelectionSettings


class RFSelectionSettings(BaseSupervisedFeatureSelectionSettings):
    """Settings for random forest selection"""

    def __init__(self, data: pd.DataFrame, target: pd.DataFrame, target_type: TargetType = None,
                 num_features: Optional[int] = None,
                 sweep_args: dict = None,
                 rf_args: Dict[str, Any] = None):
        super().__init__(data, target, target_type)
        self.rf_args = rf_args
        self.num_features = num_features
        self.sweep_args = sweep_args
