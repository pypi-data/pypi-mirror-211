"""Includes RFSelection class."""
from typing import Union, Optional

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.feature_selection.domain.objects.rf_selection_output import RFSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.rf_selection_settings import RFSelectionSettings
from organon.ml.feature_selection.domain.services.rf_selection_service import RFSelectionService
from organon.ml.feature_selection.services.abstractions.base_supervised_feature_selecter import \
    BaseSupervisedFeatureSelecter


class RFSelection(BaseSupervisedFeatureSelecter):
    """Feature selecter which utilizes random forest for selection"""

    def __init__(self, data: pd.DataFrame, target: Union[pd.DataFrame, pd.Series], target_type: str, *,
                 num_features: int = None, sweep_args: dict = None, **kwargs):
        super().__init__(data, target)
        target = self._get_target_as_df(target)
        self.settings = RFSelectionSettings(data, target, target_type=get_enum(target_type, TargetType),
                                            num_features=num_features,
                                            sweep_args=sweep_args,
                                            rf_args=kwargs)
        self.output: Optional[RFSelectionOutput] = None

    def _run(self):
        service = RFSelectionService()
        self.output = service.run_selection(self.settings)
        return self.output
