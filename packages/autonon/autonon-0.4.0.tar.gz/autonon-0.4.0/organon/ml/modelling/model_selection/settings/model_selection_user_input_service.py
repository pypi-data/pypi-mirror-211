"""Includes ModelSelectionUserInputService class."""
from typing import List

import pandas as pd

from organon.fl.core.helpers import list_helper
from organon.ml.common.enums.target_type import TargetType

from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.algorithms.core.enums.modeller import Modeller
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType
from organon.ml.modelling.model_selection.services.user_settings.user_hp_optimization_settings import \
    UserHPOptimizationSettings
from organon.ml.modelling.model_selection.services.user_settings.user_selection_settings import UserSelectionSettings
from organon.ml.modelling.model_selection.settings.enums.search_type import SearchType
from organon.ml.modelling.model_selection.settings.objects.cross_validation_settings import CrossValidationSettings
from organon.ml.modelling.model_selection.settings.objects.hp_optimization_settings import HPOptimizationSettings
from organon.ml.modelling.model_selection.settings.objects.selection_settings import SelectionSettings


class ModelSelectionUserInputService:
    """User input service for model_selection module"""

    @classmethod
    def get_selection_settings(cls, user_settings: UserSelectionSettings) -> SelectionSettings:
        """Generate SelectionSettings from UserSelectionSettings"""
        target_type = get_enum(user_settings.target_type, TargetType)
        return SelectionSettings(user_settings.modellers,
                                 user_settings.train_data, user_settings.target_data,
                                 target_type=target_type, cv_count=user_settings.cv_count,
                                 test_data=user_settings.test_data, test_target_data=user_settings.test_target_data,
                                 add_stacking=user_settings.add_stacking, add_voting=user_settings.add_voting,
                                 num_threads_for_parallel_cv=user_settings.num_threads_for_parallel_cv,
                                 num_threads_for_parallel_fit=user_settings.num_threads_for_parallel_fit)

    @classmethod
    def get_cross_validation_settings(cls, modellers: List[BaseModeller], train_data: pd.DataFrame,
                                      target_data: pd.Series, cv_count: int,
                                      bin_count, return_test_fold) -> CrossValidationSettings:
        """Generate CrossValidationSettings from settings entered by user"""
        if list_helper.is_null_or_empty(modellers):
            raise ValueError("Modellers not given")
        if train_data is None or len(train_data) == 0:
            raise ValueError("train_data cannot be empty")
        if cv_count <= 1:
            raise ValueError("cv_count should be higher than 1")

        first_modeller_type = modellers[0].modeller_type
        if first_modeller_type not in [ModellerType.CLASSIFIER, ModellerType.REGRESSOR]:
            raise ValueError("Modellers should be either classifiers or regressors")

        for modeller in modellers:
            if modeller.modeller_type != first_modeller_type:
                raise ValueError("All modellers should be of same type (classifiers or regressors)")

        if bin_count is not None and first_modeller_type != ModellerType.REGRESSOR:
            raise ValueError("bin_count is used only in regression modelling")

        return CrossValidationSettings(modellers, train_data, target_data, cv_count, bin_count, return_test_fold)

    @classmethod
    def get_hp_optimization_settings(cls, settings: UserHPOptimizationSettings) -> HPOptimizationSettings:
        """Validates settings entered by user and generates settings object for HPOService"""
        if settings.train_data is None or len(settings.train_data) == 0:
            raise ValueError("train_data should not be empty")
        if settings.target_data is None or len(settings.target_data) == 0:
            raise ValueError("target_data should not be empty")

        search_method = get_enum(settings.search_method, SearchType)

        if settings.cv_fold is None and settings.test_data is None:
            raise ValueError("Either cv_fold or test_data should be given")

        if sum(1 for data in [settings.test_data, settings.test_target_data] if data is None) == 1:
            raise ValueError("Both test_data and test_target_data should be given")

        modellers = settings.modellers
        if settings.modellers is not None:
            modellers = [get_enum(modeller, Modeller) for modeller in settings.modellers]
            if [modeller for modeller in modellers if modeller.get_modeller_type() != modellers[0].get_modeller_type()]:
                raise ValueError("Either all modellers should be classifiers or all of them should be regressors")

        if settings.modellers is not None and settings.modeller_params is not None:
            if len(settings.modeller_params) != len(settings.modellers):
                raise ValueError("Please enter parameters for all modellers. "
                                 "Enter an empty dictionary if no parameters will be added for a modeller")

        return HPOptimizationSettings(
            train_data=settings.train_data,
            target_data=settings.target_data,
            modellers=modellers,
            modeller_params=settings.modeller_params,
            search_method=search_method,
            cv_fold=settings.cv_fold,
            scoring_metrics=settings.scoring_metrics,
            test_data=settings.test_data,
            test_target_data=settings.test_target_data,
            search_params=settings.search_params)
