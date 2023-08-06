"""Includes HPOService class."""
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, PredefinedSplit, RandomizedSearchCV
from sklearn.model_selection._search import BaseSearchCV
from sklearn.pipeline import Pipeline
from skopt import BayesSearchCV

from organon.ml.modelling.algorithms.classifiers.rf_classifier import RFClassifier
from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.algorithms.core.enums.modeller import Modeller
from organon.ml.modelling.algorithms.services.algorithm_service import AlgorithmService

from organon.ml.modelling.model_selection.domain.objects.hpo_output import HPOOutput
from organon.ml.modelling.model_selection.domain.services.cross_validation_service import CrossValidationService
from organon.ml.modelling.model_selection.settings.enums.search_type import SearchType
from organon.ml.modelling.model_selection.settings.objects.hp_optimization_settings import \
    HPOptimizationSettings


class HPOService:
    """Hyperparameter optimization service"""

    @classmethod
    def execute(cls, settings: HPOptimizationSettings) -> HPOOutput:
        """Executes hyperparameter optimization with given settings and return HPOOutput"""
        is_default_search = settings.search_method is None
        if is_default_search:
            raise NotImplementedError  # analiz güncellenince eklenecek
        modellers = settings.modellers
        modeller_type = modellers[0].get_modeller_type()

        train_data = settings.train_data
        target_data = settings.target_data
        if settings.test_data is not None:
            train_data, target_data, predefined_split = cls._get_unified_data_and_split(
                train_data, target_data, settings.test_data, settings.test_target_data)
        else:
            predefined_split = CrossValidationService.get_predefined_split(settings.train_data,
                                                                           settings.target_data,
                                                                           modeller_type, cv_count=settings.cv_fold)

        modeller_instances = cls._get_modeller_instances(modellers)
        search_cv = cls._get_search_cv_instance(settings.search_method,
                                                modeller_instances, settings.modeller_params,
                                                predefined_split,
                                                settings.search_params, settings.scoring_metrics)
        search_cv.fit(train_data, target_data)

        output = cls._get_output(settings.train_data, settings.target_data, search_cv, modeller_instances)
        return output

    @classmethod
    def _get_search_cv_instance(cls, search_method: SearchType, modeller_instances, modeller_params,
                                predefined_split: PredefinedSplit,
                                search_params=None, scoring_metrics: List[str] = None) -> BaseSearchCV:
        cv_class = cls._validate_and_get_cv_class(search_method, search_params, scoring_metrics)
        params = cls._get_pipeline_params([tpl[1] for tpl in modeller_instances], modeller_params)

        pipeline = Pipeline([('mdl', RFClassifier())])  # placeholder classifier
        search_params = search_params if search_params is not None else {}
        scoring_metrics = scoring_metrics[0] \
            if scoring_metrics is not None and len(scoring_metrics) == 1 else scoring_metrics
        grid = cv_class(pipeline, params, cv=predefined_split, scoring=scoring_metrics,
                        refit=False, **search_params)
        return grid

    @classmethod
    def _get_output(cls, train_data: pd.DataFrame, target_data: pd.Series, search_cv: BaseSearchCV,
                    modeller_instances) -> HPOOutput:
        output = HPOOutput()
        output.best_modeller, output.best_params = cls._get_best_modeller_and_params(search_cv)
        output.best_modeller.set_params(**output.best_params)
        output.best_modeller.fit(train_data, target_data)
        output.summary = cls._get_metrics(search_cv, modeller_instances)
        return output

    @classmethod
    def _get_modeller_instances(cls, modellers: Union[List[Modeller]]):
        modeller_instances = [(modeller.name, AlgorithmService.get_modeller(modeller))
                              for modeller in modellers]
        return modeller_instances

    @classmethod
    def _get_best_modeller_and_params(cls, grid: BaseSearchCV):
        """return best modeller and its parameters."""
        # If there are multiple metrics, metrics are compared in order.
        # If there are two params with same score in first metric, next metric will be used for comparison
        results = grid.cv_results_
        scoring_metrics_list = ["score"] if not isinstance(grid.scoring, list) else grid.scoring

        all_mean_scores = []
        for i in range(len(results[f"mean_test_{scoring_metrics_list[0]}"])):
            param_mean_scores = []
            for metric in scoring_metrics_list:
                param_mean_scores.append(results[f"mean_test_{metric}"][i])
            all_mean_scores.append((i, param_mean_scores))
        all_mean_scores = sorted(all_mean_scores, key=lambda tpl: tpl[1], reverse=True)
        best_modeller, best_params = cls._get_params_with_actual_names(results["params"][all_mean_scores[0][0]])
        return best_modeller, best_params

    @classmethod
    def _get_metrics(cls, grid: BaseSearchCV, modeller_instances: List[Tuple[str, BaseModeller]]):
        scoring_metrics_list = ["score"] if not isinstance(grid.scoring, list) else grid.scoring
        cv_results = grid.cv_results_
        metrics = []
        num_splits = grid.n_splits_
        mean_metric_strings = []
        for i, params in enumerate(cv_results["params"]):
            modeller, params = cls._get_params_with_actual_names(params)
            res = {
                "modeller": next(tpl[0] for tpl in modeller_instances if tpl[1] == modeller),
                "params": params
            }
            for metric in scoring_metrics_list:
                mean_metric_str = metric
                if num_splits > 1:
                    mean_metric_str = f"mean {metric}"
                    for split_index in range(num_splits):
                        res[f"fold-{split_index} {metric}"] = cv_results[f"split{split_index}_test_{metric}"][i]
                res[mean_metric_str] = cv_results[f"mean_test_{metric}"][i]
                if mean_metric_str not in mean_metric_strings:
                    mean_metric_strings.append(mean_metric_str)
            metrics.append(res)
        frame = pd.DataFrame(metrics).sort_values(by=mean_metric_strings, ascending=False, ignore_index=True)

        return frame

    @classmethod
    def _get_params_with_actual_names(cls, grid_params_dict: dict) -> Tuple[BaseModeller, dict]:
        params = grid_params_dict.copy()
        best_modeller = params.pop("mdl")
        best_params = {param.split("mdl__")[1]: value for param, value in params.items()}
        return best_modeller, best_params

    @classmethod
    def _validate_and_get_cv_class(cls, search_method: SearchType, search_params: dict, scoring_metrics: List[str]):
        invalid_search_params = ["estimator", "cv", "scoring", "refit"]

        if search_method == SearchType.GRID:
            cv_class = GridSearchCV
            invalid_search_params.extend(["param_grid"])
        elif search_method == SearchType.RANDOM:
            cv_class = RandomizedSearchCV
            invalid_search_params.extend(["param_distributions"])
        else:
            cv_class = BayesSearchCV
            invalid_search_params.extend(["search_spaces"])

        if cv_class == BayesSearchCV and isinstance(scoring_metrics, list) and len(scoring_metrics) > 1:
            raise ValueError("Model Based Search cannot be run with multiple scoring metrics")

        if search_params is not None:
            invalid_entered_params = [param for param in search_params if param in invalid_search_params]
            if len(invalid_entered_params) > 0:
                raise ValueError(f"search_params cannot include these params: {','.join(invalid_entered_params)}")
        return cv_class

    @classmethod
    def _get_pipeline_params(cls, modeller_instances: List[BaseModeller],
                             modeller_params: List[Dict[str, list]]) -> List[Dict[str, list]]:
        all_params = []
        if modeller_params is None:
            modeller_params = [{} for _ in modeller_instances]
        for modeller, params_dict in zip(modeller_instances, modeller_params):
            new_params_dict = {"mdl": [modeller]}
            for param, list_of_values in params_dict.items():
                new_params_dict[f"mdl__{param}"] = list_of_values
            all_params.append(new_params_dict)
        return all_params

    @classmethod
    def _get_unified_data_and_split(cls, train_data: pd.DataFrame, train_target_data: pd.Series,
                                    test_data: pd.DataFrame,
                                    test_target_data: pd.Series) -> Tuple[pd.DataFrame, pd.Series,
                                                                          PredefinedSplit]:
        len_train = len(train_data)
        len_test = len(test_data)
        union_data = pd.concat([train_data, test_data], copy=False, ignore_index=True)
        union_target_data = pd.concat([train_target_data, test_target_data], copy=False, ignore_index=True)

        len_union = len_test + len_train
        test_fold = np.full(len_union, -1)
        test_fold[len_train:] = 1
        return union_data, union_target_data, PredefinedSplit(test_fold)
