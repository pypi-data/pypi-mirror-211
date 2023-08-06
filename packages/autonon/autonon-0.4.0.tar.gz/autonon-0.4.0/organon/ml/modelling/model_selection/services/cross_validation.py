"""Includes CrossValidation class"""
from typing import List

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.model_selection.domain.objects.cross_validation_output import CrossValidationOutput
from organon.ml.modelling.model_selection.domain.services.cross_validation_service import CrossValidationService, \
    DEFAULT_CV_COUNT
from organon.ml.modelling.model_selection.settings.model_selection_user_input_service import \
    ModelSelectionUserInputService


class CrossValidation:
    """Class for comparison of multiple modellers after fitting with the cross validation"""

    def __init__(self, modellers: List[BaseModeller], train_data: pd.DataFrame,
                 target_data: pd.Series, cv_count: int = DEFAULT_CV_COUNT, bin_count=None, return_test_fold=False):
        self.settings = ModelSelectionUserInputService.get_cross_validation_settings(modellers, train_data,
                                                                                     target_data, cv_count, bin_count,
                                                                                     return_test_fold)
        self.output: CrossValidationOutput = None

    def execute(self):
        """Fits modellers and returns scores for every run of every modeller"""
        output = CrossValidationService.execute(self.settings)
        self.output = output
        return output
