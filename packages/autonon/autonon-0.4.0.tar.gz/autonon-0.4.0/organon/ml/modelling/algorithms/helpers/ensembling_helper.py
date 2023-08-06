"""Includes helper functions for ensembling"""
from typing import List, Union

import numpy as np
import pandas as pd

from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType


def get_voting_prediction(all_predictions: Union[pd.DataFrame, np.ndarray], modeller_type: ModellerType) -> pd.Series:
    """Returns prediction after applying voting on 'all_predictions' which stores different predictions as columns"""
    if modeller_type == ModellerType.REGRESSOR:
        return get_voting_regressor_prediction(all_predictions)
    if modeller_type == ModellerType.CLASSIFIER:
        return get_voting_classifier_prediction(all_predictions)
    raise NotImplementedError


def get_voting_classifier_prediction(all_predictions: Union[pd.DataFrame, np.ndarray]) -> pd.Series:
    """Returns prediction after applying voting on 'all_predictions' which stores different predictions as columns"""
    final_pred = np.apply_along_axis(_get_most_observed_val, axis=1, arr=all_predictions)
    if final_pred.ndim > 1:
        final_pred = final_pred[:, 0]
    return pd.Series(final_pred)


def get_voting_regressor_prediction(all_predictions: Union[pd.DataFrame, np.ndarray]) -> pd.Series:
    """Returns prediction after applying voting on 'all_predictions' which stores different predictions as columns"""
    final_pred = np.mean(all_predictions, axis=1)
    return pd.Series(final_pred)


def get_voting_predict_proba(proba_dfs: List[pd.DataFrame]):
    """Returns probabilities after applying voting on 'proba_dfs' where every dataframe is calculated
    by a different modeller"""
    columns = proba_dfs[0].columns.tolist()
    proba_dfs = [proba_df.loc[:, columns] for proba_df in proba_dfs]
    average_probas = sum(proba_dfs) / len(proba_dfs)
    return average_probas


def _get_most_observed_val(arr: np.array):
    """returns most observed value in array. If there are two with same number of occurrences, chooses randomly"""
    unique, counts = np.unique(arr, return_counts=True)
    indices = np.where(counts == max(counts))
    if len(indices[0]) > 1:
        return np.random.choice(unique[indices], 1)
    return unique[indices][0]
