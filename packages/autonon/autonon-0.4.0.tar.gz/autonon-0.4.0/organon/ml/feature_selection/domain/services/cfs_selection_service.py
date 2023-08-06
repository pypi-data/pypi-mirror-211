"""Includes CFSSelectionService class."""
from typing import Dict

import numpy as np
import pandas as pd
from scipy.stats import pointbiserialr

from organon.fl.core.helpers.data_frame_helper import get_correlation_matrix_memory_efficient
from organon.fl.mathematics.constants import DOUBLE_MIN
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.cfs_selection_output import CFSSelectionOutput
from organon.ml.feature_selection.domain.objects.priority_queue import PriorityQueue
from organon.ml.feature_selection.domain.objects.settings.cfs_selection_settings import CFSSelectionSettings
from organon.ml.feature_selection.domain.services.base_feature_selection_service import SelectionRunSettings
from organon.ml.feature_selection.domain.services.base_supervised_feature_selection_service import \
    BaseSupervisedFeatureSelectionService


class CFSSelectionService(BaseSupervisedFeatureSelectionService[CFSSelectionSettings, CFSSelectionOutput]):
    """Service class for CFS selection"""

    @classmethod
    def _validate_settings(cls, settings: CFSSelectionSettings):
        if settings.target_type not in [TargetType.BINARY, TargetType.SCALAR]:
            raise ValueError("Correlation based feature selection works only for BINARY or SCALAR targets")

    @classmethod
    def _run(cls, run_settings: SelectionRunSettings) -> CFSSelectionOutput:
        target = cls._get_target_data_as_series_of_numbers(run_settings.settings)
        settings: CFSSelectionSettings = run_settings.settings
        data = run_settings.data
        features = data.columns
        queue = PriorityQueue()

        visited = []
        # counter for backtracks
        n_backtrack = 0
        # limit of backtracks
        max_backtracks = run_settings.settings.max_backtracks
        corr_dict, best_value, best_feature = cls._get_feature_class_correlations(data, target)
        queue.push({best_feature}, best_value)
        best_subset = set()
        corr_matrix = cls._get_correlation_matrix(data, settings.prioritize_performance)
        while not queue.is_empty():
            # get element of queue with highest merit
            subset, priority = queue.pop()

            # check whether the priority of this subset
            # is higher than the current best subset
            if priority < best_value:
                n_backtrack += 1
            else:
                best_value = priority
                best_subset = subset

            # goal condition
            if n_backtrack == max_backtracks:
                break

            # iterate through all features and look of one can
            # increase the merit
            for feature in features:
                if feature in subset:
                    continue
                temp_subset = subset.copy()
                temp_subset.add(feature)

                # check if this subset has already been evaluated
                for node in visited:
                    if node == temp_subset:
                        break
                # if not, ...
                else:
                    # ... mark it as visited
                    visited.append(temp_subset)
                    # ... compute merit
                    merit = cls._get_merit(temp_subset, corr_dict, corr_matrix)
                    # and push it to the queue
                    queue.push(temp_subset, merit)
        output = CFSSelectionOutput()
        output.selected_features = list(best_subset)
        return output

    @classmethod
    def _get_merit(cls, subset: set, corr_dict: Dict[str, float], corr_matrix):
        k = len(subset)
        # average feature-class correlation
        rcf = np.mean([corr_dict[feature] for feature in subset])

        # average feature-feature correlation
        corr = abs(corr_matrix.loc[list(subset), list(subset)])
        rff = corr.unstack().mean()

        return (k * rcf) / np.sqrt(k + k * (k - 1) * rff)

    @classmethod
    def _get_feature_class_correlations(cls, data: pd.DataFrame, target: pd.Series):
        corr_dict = {}
        best_value = DOUBLE_MIN
        best_feature = None
        for feature in data.columns:
            coeff = pointbiserialr(target, data[feature])
            val = abs(coeff.correlation)
            corr_dict[feature] = val
            if val > best_value:
                best_value = val
                best_feature = feature
        return corr_dict, best_value, best_feature

    @classmethod
    def _get_correlation_matrix(cls, data: pd.DataFrame, prioritize_performance: bool):
        if prioritize_performance:
            corr_df = data.corr()
            corr_df.values[np.tril_indices_from(corr_df.values)] = np.nan
            return corr_df
        return get_correlation_matrix_memory_efficient(data, only_half_filled=True, diagonal_values=np.nan)
