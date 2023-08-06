"""Includes LassoSelection class."""
from typing import Union, Optional

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.feature_selection.domain.objects.lasso_selection_output import LassoSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.lasso_selection_settings import LassoSelectionSettings
from organon.ml.feature_selection.domain.services.lasso_selection_service import LassoSelectionService
from organon.ml.feature_selection.services.abstractions.base_supervised_feature_selecter import \
    BaseSupervisedFeatureSelecter


class LassoSelection(BaseSupervisedFeatureSelecter):
    """Feature selecter which utilizes Lasso for selection"""

    def __init__(self, data: pd.DataFrame, target: Union[pd.DataFrame, pd.Series], target_type:str, **kwargs):
        super().__init__(data, target)
        target = self._get_target_as_df(target)
        self.settings = LassoSelectionSettings(data, target, target_type=get_enum(target_type, TargetType),
                                               lasso_args=kwargs)
        self.output: Optional[LassoSelectionOutput] = None

    def _run(self):
        service = LassoSelectionService()
        self.output = service.run_selection(self.settings)
        return self.output
