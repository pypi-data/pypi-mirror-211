"""Includes helper functions to sample, manipulate dataframes"""
from typing import List

import numpy as np
import pandas as pd

from organon.fl.core.helpers import list_helper


def get_train_test_split(data: pd.DataFrame, test_ratio: float, strata_columns: List[str] = None, random_state=None):
    """Divides given data to two splits(train and test) using given ratio"""
    if test_ratio > 1.0:
        raise ValueError("test_ratio cannot be higher than 1.0")
    test_indices = get_sample_indices(data, test_ratio, strata_columns=strata_columns, random_state=random_state)
    train_data = data.loc[data.index.difference(test_indices)]
    return train_data, data.loc[test_indices]


def get_train_test_split_from_strata(data: pd.DataFrame, strata_data: pd.Series, test_ratio: float, random_state=None):
    """Divides given data to two splits(train and test) using given ratio"""
    if test_ratio > 1.0:
        raise ValueError("test_ratio cannot be higher than 1.0")
    test_indices = get_sample_indices_from_series(strata_data, test_ratio, random_state=random_state)
    return data.loc[data.index.difference(test_indices)], strata_data.loc[strata_data.index.difference(test_indices)],\
           data.loc[test_indices], strata_data.loc[test_indices]


def get_sample_indices_from_series(strata_data: pd.Series, frac: float, replace=False, random_state=None):
    """
    Samples data and returns indices of selected rows.
    """
    return strata_data.groupby(strata_data, group_keys=False).sample(frac=frac, replace=replace,
                                                                    random_state=random_state).index


def get_sample_indices(data: pd.DataFrame, frac: float, strata_columns: List[str] = None, replace=False,
                       random_state=None):
    """
    Samples data and returns indices of selected rows.
    """
    if not list_helper.is_null_or_empty(strata_columns):
        if len([col for col in data.columns if col not in strata_columns]) > 0:
            data = data[strata_columns]
        indices = data.groupby(strata_columns, group_keys=False).sample(frac=frac, replace=replace,
                                                                        random_state=random_state).index
    else:
        indices = data.sample(frac=frac, replace=replace, random_state=random_state).index
    return indices


def get_sample_data(data: pd.DataFrame, frac: float, strata_columns: List[str] = None, replace=False,
                    random_state=None):
    """Samples data and returns new dataframe"""
    return data.loc[
        get_sample_indices(data, frac, strata_columns=strata_columns, replace=replace, random_state=random_state)]


def get_bins(data: pd.Series, num_bins: int) -> pd.Series:
    """Splits given data into given number of bins and returns bin numbers for every row"""
    sorted_indices = data.sort_values().index
    len_index = len(sorted_indices)
    num_rows_per_bin = int(len_index / num_bins)
    remaining = len_index % num_bins
    arr = np.empty(len_index)
    curr_index = 0
    for i in range(num_bins):
        step = num_rows_per_bin + 1 if i < remaining else num_rows_per_bin
        arr[curr_index:curr_index + step] = i
        curr_index = curr_index + step

    return pd.Series(arr, index=sorted_indices, dtype="category").astype(np.int8).sort_index()
