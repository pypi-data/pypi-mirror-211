"""This module includes helper functions for preprocessing"""
import numpy as np
import pandas as pd


def convert_str_series_to_binary(data: pd.Series, positive_class: str, negative_class: str) -> pd.Series:
    """convert string type series to binary values by given positive and negative classes"""
    if data is None or data.empty:
        raise ValueError("Data is None or empty.")
    if data.nunique(dropna=False) != 2:
        raise ValueError("Target column class count is not equal to 2.")
    if set(data.unique().tolist()) != {positive_class, negative_class}:
        raise ValueError("Target column classes do not match with the given positive and negative classes.")
    res_data = pd.Series(1, index=data.index, dtype=np.uint8)
    res_data.loc[data == negative_class] = 0
    return res_data


def convert_binary_series_to_str(data: pd.Series, positive_class: str, negative_class: str) -> pd.Series:
    """convert binary type series to string values by given positive and negative classes"""
    if data is None or data.empty:
        raise ValueError("Data is None or empty.")
    if data.nunique(dropna=False) != 2:
        raise ValueError("Target column class count is not equal to 2.")
    if set(data.unique().tolist()) != {0, 1}:
        raise ValueError("Target column is not binary.")
    res_data = pd.Series(positive_class, index=data.index, dtype=str)
    res_data.loc[data == 0] = negative_class
    return res_data
