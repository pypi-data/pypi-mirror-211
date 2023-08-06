"""
Built-in datasets for demonstration, educational and test purposes.
"""
import os

import pandas


def base_df():
    """
    Returns: "base" pandas.DataFrame
    """
    data_df = _get_dataset("base_df")
    return data_df.set_index(data_df.columns[0])  # pylint: disable=no-member


def score_df():
    """
    Returns: "score" pandas.DataFrame
    """
    data_df = _get_dataset("score_df")
    return data_df.set_index(data_df.columns[0])  # pylint: disable=no-member


def cash_df():
    """
    Returns: "cash" pandas.DataFrame
    """
    data_df = _get_dataset("cash_df")
    return data_df.set_index(data_df.columns[0])  # pylint: disable=no-member


def _get_dataset(dataset_name):
    return pandas.read_csv(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            dataset_name + ".zip",
        )
    )
