"""Includes LassoSelectionSettings class"""
from typing import Any, Dict

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.settings.base_supervised_feature_selection_settings import \
    BaseSupervisedFeatureSelectionSettings


class LassoSelectionSettings(BaseSupervisedFeatureSelectionSettings):
    """Settings for lasso selection service"""

    def __init__(self, data: pd.DataFrame, target: pd.DataFrame, target_type: TargetType = None,
                 lasso_args: Dict[str, Any] = None):
        super().__init__(data, target, target_type)
        self.lasso_args = lasso_args
