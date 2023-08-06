"""Includes SelectionService class."""
import threading
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

from organon.fl.core.executionutil import parallel_execution_helper
from organon.fl.core.executionutil.objects.locked_iterator import LockedIterator
from organon.fl.mathematics.constants import DOUBLE_MIN
from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers import validation_helper
from organon.ml.modelling.algorithms.classifiers.gam_classifier import GamClassifier
from organon.ml.modelling.algorithms.classifiers.rf_classifier import RFClassifier
from organon.ml.modelling.algorithms.classifiers.stacking_ensemble_classifier import StackingEnsembleClassifier
from organon.ml.modelling.algorithms.classifiers.voting_ensemble_classifier import VotingEnsembleClassifier
from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType
from organon.ml.modelling.algorithms.regressors.gam_regressor import GamRegressor
from organon.ml.modelling.algorithms.regressors.stacking_ensemble_regressor import StackingEnsembleRegressor
from organon.ml.modelling.algorithms.regressors.voting_ensemble_regressor import VotingEnsembleRegressor
from organon.ml.modelling.model_selection.domain.objects.selecter_output import SelecterOutput
from organon.ml.modelling.model_selection.domain.services.cross_validation_service import CrossValidationService
from organon.ml.modelling.model_selection.settings.objects.selection_settings import SelectionSettings


class SelectionService:
    """Service for selecting best modeller from a list of modellers"""

    @classmethod
    def select(cls, settings: SelectionSettings) -> SelecterOutput:
        """Selects best modeller from a list of modellers"""
        modeller_type = cls._run_initial_validation(settings)
        use_cv = settings.test_data is None
        fitted_stacking_modeller = None
        fitted_voting_modeller = None
        fitted_modellers = None
        if use_cv:
            pds = CrossValidationService.get_predefined_split(settings.train_data, settings.target_data,
                                                              modeller_type, cv_count=settings.cv_count)
            split_generator = LockedIterator(pds.split())
            all_scores = [None] * settings.cv_count
            if settings.num_threads_for_parallel_cv is not None:
                num_threads = cls.__get_num_threads(settings.num_threads_for_parallel_cv, settings.cv_count)
                params = [(all_scores, i, settings, split_generator) for i in range(settings.cv_count)]
                parallel_execution_helper.execute_parallel(params, cls._get_scores_for_split, num_jobs=num_threads,
                                                           require_shared_memory=True)
            else:
                for i in range(settings.cv_count):
                    cls._get_scores_for_split(all_scores, i, settings, split_generator)
        else:
            scores, fitted_modellers, fitted_stacking_modeller, fitted_voting_modeller = \
                cls._get_scores(settings, settings.train_data,
                                settings.target_data,
                                settings.test_data,
                                settings.test_target_data)
            all_scores = [scores]

        output = SelecterOutput()
        output.modeller_fold_scores = np.array([scores["modellers"] for scores in all_scores]).T.tolist()
        output.modeller_scores = list(np.mean(output.modeller_fold_scores, axis=1))

        stacking_mean_score, voting_mean_score = cls._fill_output_for_stacking_and_voting(all_scores, output,
                                                                                          settings.add_stacking,
                                                                                          settings.add_voting)
        all_mean_scores = output.modeller_scores + [stacking_mean_score, voting_mean_score]

        output.best_modeller = cls._get_best_modeller_as_fitted(settings, all_mean_scores, fitted_modellers,
                                                                fitted_stacking_modeller,
                                                                fitted_voting_modeller)

        return output

    @classmethod
    def _get_scores_for_split(cls, all_scores, i, settings: SelectionSettings, split_generator):
        train_indices, test_indices = next(split_generator)
        scores, _, _, _ = cls._get_scores(settings,
                                          settings.train_data.iloc[train_indices],
                                          settings.target_data.iloc[train_indices],
                                          settings.train_data.iloc[test_indices],
                                          settings.target_data.iloc[test_indices])
        all_scores[i] = scores

    @classmethod
    def _run_initial_validation(cls, settings: SelectionSettings):
        if settings.cv_count is None and settings.test_data is None:
            raise ValueError("Give a cv_count or test_data")

        modeller_type = settings.modellers[0].modeller_type
        if [modeller for modeller in settings.modellers if modeller.modeller_type != modeller_type]:
            raise ValueError("All modellers should be of same type")
        if modeller_type not in [ModellerType.CLASSIFIER, ModellerType.REGRESSOR]:
            raise ValueError("Only classifiers and regressors are supported in selection service")

        validation_helper.validate_get_target_type(modeller_type, settings.target_type)
        return modeller_type

    @classmethod
    def _fill_output_for_stacking_and_voting(cls, all_scores, output: SelecterOutput, add_stacking: bool,
                                             add_voting: bool):
        stacking_mean_score = DOUBLE_MIN
        if add_stacking:
            output.stacking_fold_scores = [scores["stacking"] for scores in all_scores]
            stacking_mean_score = np.mean(np.array(output.stacking_fold_scores))
            output.stacking_score = stacking_mean_score

        voting_mean_score = DOUBLE_MIN
        if add_voting:
            output.voting_fold_scores = [scores["voting"] for scores in all_scores]
            voting_mean_score = np.mean(np.array(output.voting_fold_scores))
            output.voting_score = voting_mean_score
        return stacking_mean_score, voting_mean_score

    @classmethod
    def _fit_and_append_model(cls, fitted_modellers, modeller, i, train_data, target_data):
        modeller = modeller.clone()
        modeller.fit(train_data, target_data)
        fitted_modellers[i] = modeller

    @classmethod
    def _get_best_modeller_as_fitted(cls, settings: SelectionSettings, all_mean_scores: List[float],
                                     fitted_modellers: Optional[List[BaseModeller]],
                                     fitted_stacking_modeller: Optional[BaseModeller],
                                     fitted_voting_modeller: Optional[BaseModeller]) -> BaseModeller:
        modeller_type = settings.modellers[0].modeller_type
        max_score = max(all_mean_scores)
        max_score_index = all_mean_scores.index(max_score)
        is_stacking_best = max_score_index == len(all_mean_scores) - 2
        is_voting_best = max_score_index == len(all_mean_scores) - 1

        cv_used = fitted_modellers is None

        if not cv_used:
            if is_stacking_best:
                return fitted_stacking_modeller
            if is_voting_best:
                return fitted_voting_modeller
            return fitted_modellers[max_score_index]

        best_modeller = None

        if is_stacking_best or is_voting_best:
            # if cv is used, modellers should be fitted with whole train data to be used as
            # estimators in stacking or voting
            fitted_modellers = [None] * len(settings.modellers)

            if settings.num_threads_for_parallel_fit is not None:
                num_threads = cls.__get_num_threads(settings.num_threads_for_parallel_fit, len(settings.modellers))
                params = [(fitted_modellers, modeller, i, settings.train_data, settings.target_data)
                          for i, modeller in enumerate(settings.modellers)]
                parallel_execution_helper.execute_parallel(params, cls._fit_and_append_model, num_jobs=num_threads,
                                                           require_shared_memory=True)
            else:
                for i, modeller in enumerate(settings.modellers):
                    cls._fit_and_append_model(fitted_modellers, modeller, i, settings.train_data, settings.target_data)

            if is_stacking_best:
                best_modeller = cls._get_stacking_modeller(fitted_modellers, modeller_type, settings.target_type)
                best_modeller.fit(settings.train_data, settings.target_data)

            elif is_voting_best:
                best_modeller = cls._get_voting_modeller(fitted_modellers, modeller_type)
                best_modeller.fit(settings.train_data, settings.target_data)
        else:
            best_modeller = settings.modellers[max_score_index].clone().fit(settings.train_data,
                                                                            settings.target_data)

        return best_modeller

    @classmethod
    def _fit_and_score_models(cls, fitted_modellers: list, modeller: BaseModeller,
                              fit_data: Tuple[pd.DataFrame, pd.Series],
                              score_data: Tuple[pd.DataFrame, pd.Series],
                              modeller_scores_for_fold: list, add_voting: bool,
                              all_predictions_df: pd.DataFrame, modeller_index: int, df_write_lock: threading.Lock):
        # pylint: disable=too-many-arguments
        modeller = modeller.clone()
        modeller.fit(fit_data[0], fit_data[1])
        fitted_modellers[modeller_index] = modeller

        score = modeller.score(score_data[0], score_data[1])
        modeller_scores_for_fold[modeller_index] = score
        if add_voting:
            prediction_df = modeller.predict(score_data[0])
            with df_write_lock:
                all_predictions_df[f"mdl_{modeller_index}"] = prediction_df[prediction_df.columns[0]].values

    @classmethod
    def _get_scores(cls, settings: SelectionSettings, train_data: pd.DataFrame, target_data: pd.Series,
                    test_data, test_target_data):
        all_predictions_df = pd.DataFrame()
        stacking_score = None
        voting_score = None
        modeller_type = settings.modellers[0].modeller_type
        fitted_modellers = [None] * len(settings.modellers)
        modeller_scores_for_fold = [None] * len(settings.modellers)
        df_write_lock = threading.Lock()
        if settings.num_threads_for_parallel_fit is not None:
            num_threads = cls.__get_num_threads(settings.num_threads_for_parallel_fit, len(settings.modellers))
            params = [(fitted_modellers, modeller, (train_data, target_data), (test_data, test_target_data),
                       modeller_scores_for_fold, settings.add_voting, all_predictions_df, i, df_write_lock)
                      for i, modeller in enumerate(settings.modellers)]
            parallel_execution_helper.execute_parallel(params, cls._fit_and_score_models, num_jobs=num_threads,
                                                       require_shared_memory=True)
        else:
            for i, modeller in enumerate(settings.modellers):
                cls._fit_and_score_models(fitted_modellers, modeller, (train_data, target_data),
                                          (test_data, test_target_data),
                                          modeller_scores_for_fold, settings.add_voting,
                                          all_predictions_df, i, df_write_lock)

        stacking_modeller = None
        if settings.add_stacking:
            stacking_modeller = cls._get_stacking_modeller(fitted_modellers,
                                                           modeller_type, settings.target_type)
            stacking_modeller.fit(train_data, target_data)
            stacking_score = stacking_modeller.score(test_data, test_target_data)

        voting_modeller = None
        if settings.add_voting:
            voting_modeller = cls._get_voting_modeller(fitted_modellers, modeller_type)
            voting_modeller.fit(train_data, target_data)
            voting_score = voting_modeller.score(test_data, test_target_data)

        return {"modellers": modeller_scores_for_fold, "stacking": stacking_score, "voting": voting_score}, \
               fitted_modellers, stacking_modeller, voting_modeller

    @classmethod
    def __get_num_threads(cls, num_threads: int, default=None):
        if num_threads == -1:
            if default is not None:
                return default
            return None
        return num_threads

    @classmethod
    def _get_stacking_modeller(cls, modellers, modeller_type: ModellerType, target_type: TargetType) -> BaseModeller:
        named_modellers = [(f"mdl_{i}", modeller) for i, modeller in enumerate(modellers)]
        if modeller_type == ModellerType.CLASSIFIER:
            final_estimator = RFClassifier() if target_type == TargetType.MULTICLASS else GamClassifier()
            return StackingEnsembleClassifier(estimators=named_modellers, final_estimator=final_estimator,
                                              cv="prefit", stack_method="predict_proba")
        return StackingEnsembleRegressor(estimators=named_modellers, final_estimator=GamRegressor(),
                                         cv="prefit")

    @classmethod
    def _get_voting_modeller(cls, modellers, modeller_type: ModellerType) -> BaseModeller:
        if modeller_type == ModellerType.CLASSIFIER:
            return VotingEnsembleClassifier(estimators=modellers, prefit=True)
        return VotingEnsembleRegressor(estimators=modellers, prefit=True)
