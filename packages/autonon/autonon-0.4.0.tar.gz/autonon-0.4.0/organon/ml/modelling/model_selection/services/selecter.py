"""Includes Selecter class"""
from typing import List

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.model_selection.domain.objects.selecter_output import SelecterOutput
from organon.ml.modelling.model_selection.domain.services.selection_service import SelectionService
from organon.ml.modelling.model_selection.services.user_settings.user_selection_settings import UserSelectionSettings
from organon.ml.modelling.model_selection.settings.model_selection_user_input_service import \
    ModelSelectionUserInputService


class Selecter:
    """Best model selecter"""

    def __init__(self, modellers: List[BaseModeller], train_data: pd.DataFrame, target_data: pd.Series, *,
                 target_type: str = None, cv_count: int = 5,
                 test_data: pd.DataFrame = None, test_target_data: pd.Series = None,
                 add_stacking=True, add_voting=True, num_threads_for_parallel_fit:int=None,
                 num_threads_for_parallel_cv:int=None):
        # pylint: disable=too-many-arguments
        user_settings = UserSelectionSettings(modellers, train_data, target_data, target_type,
                                              cv_count, test_data, test_target_data, add_stacking, add_voting,
                                              num_threads_for_parallel_fit, num_threads_for_parallel_cv)
        self.settings = ModelSelectionUserInputService.get_selection_settings(user_settings)
        self.output: SelecterOutput = None

    def select(self):
        """Executes selecter and returns output"""
        service = SelectionService()
        self.output = service.select(self.settings)
        return self.output
