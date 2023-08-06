"""Includes HPOptimizer class."""
from typing import List, Dict, Optional

import pandas as pd

from organon.ml.modelling.algorithms.services.ml_application_operations import MLApplicationOperations
from organon.ml.modelling.model_selection.domain.objects.hpo_output import HPOOutput
from organon.ml.modelling.model_selection.domain.services.cross_validation_service import DEFAULT_CV_COUNT
from organon.ml.modelling.model_selection.domain.services.hpo_service import HPOService
from organon.ml.modelling.model_selection.services.user_settings.user_hp_optimization_settings import \
    UserHPOptimizationSettings
from organon.ml.modelling.model_selection.settings.enums.search_type import SearchType
from organon.ml.modelling.model_selection.settings.model_selection_user_input_service import \
    ModelSelectionUserInputService


class HPOptimizer:
    """Hyper parameter optimizer"""

    def __init__(self):
        MLApplicationOperations.initialize_app()
        self.output = None

    def execute(self, train_data: pd.DataFrame, target_data: pd.Series, test_data: pd.DataFrame = None,
                test_target_data: pd.Series = None, cv_fold: int = DEFAULT_CV_COUNT,
                modellers: List[str] = None, modeller_params: List[Dict[str, list]] = None,
                search_method: str = SearchType.RANDOM.name, search_params: dict = None,
                scoring_metrics: Optional[List[str]] = None
                ) -> HPOOutput:
        """
        Execute optimizer and return output
        todo parametre açıklamaları
        """
        # pylint: disable=too-many-arguments

        user_settings = UserHPOptimizationSettings(train_data, target_data, search_method,
                                                   modellers=modellers, modeller_params=modeller_params,
                                                   cv_fold=cv_fold, test_data=test_data,
                                                   test_target_data=test_target_data,
                                                   scoring_metrics=scoring_metrics,
                                                   search_params=search_params)
        settings = ModelSelectionUserInputService().get_hp_optimization_settings(user_settings)
        self.output = HPOService().execute(settings)
        return self.output
