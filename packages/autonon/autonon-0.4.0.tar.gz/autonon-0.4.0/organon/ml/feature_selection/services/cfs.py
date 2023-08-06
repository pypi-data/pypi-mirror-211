"""Includes CFS class."""
from typing import Union, Optional

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.feature_selection.domain.objects.cfs_selection_output import CFSSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.cfs_selection_settings import CFSSelectionSettings
from organon.ml.feature_selection.domain.services.cfs_selection_service import CFSSelectionService
from organon.ml.feature_selection.services.abstractions.base_supervised_feature_selecter import \
    BaseSupervisedFeatureSelecter


class CFS(BaseSupervisedFeatureSelecter):
    """Feature selecter which utilizes a correlation based feature selection algorithm"""

    def __init__(self, data: pd.DataFrame, target: Union[pd.DataFrame, pd.Series], target_type:str, *,
                 max_backtracks: int = 5, prioritize_performance=False):
        super().__init__(data, target)
        target = self._get_target_as_df(target)
        self.settings = CFSSelectionSettings(data, target, get_enum(target_type, TargetType),
                                             max_backtracks=max_backtracks,
                                             prioritize_performance=prioritize_performance)
        self.output: Optional[CFSSelectionOutput] = None

    def _run(self):
        service = CFSSelectionService()
        self.output = service.run_selection(self.settings)
        return self.output
