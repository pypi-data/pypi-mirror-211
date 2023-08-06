"""
This module includes helper functions for pandas DataFrames.
"""
from typing import List, Dict

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype, is_string_dtype, is_datetime64_any_dtype

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.executionutil import parallel_execution_helper
from organon.fl.core.helpers.object_helper import get_attribute_dict


def objects_to_data_frame(objects: List[object], column_name_map: Dict[str, str] = None) -> pd.DataFrame:
    """
    Converts list of objects to DataFrame
    :param column_name_map: dictionary to map attribute names to dataframe column names
    :param objects: List of objects
    """
    if column_name_map is None:
        column_name_map = {i: i for i in list(get_attribute_dict(objects[0]).keys())}
        # columns = list(objects[0].__dict__.keys())
    data_frame = pd.DataFrame(columns=list(column_name_map.values()))
    for obj in objects:
        obj_dict = get_attribute_dict(obj)
        values_dict = {column_name_map[attr]: obj_dict[attr] for attr in column_name_map}
        data_frame = data_frame.append(values_dict, ignore_index=True)
    return data_frame


def dataframe_to_objects(data_frame: pd.DataFrame, cls, column_name_map: Dict[str, str] = None):
    """
    Converts the given data frame to list of objects of given class.
    :param data_frame:
    :param cls: Class of objects
    :param column_name_map: map of attribute names to dataframe column names
    :return: List of objects of given class
    """
    if column_name_map is None:
        column_name_map = {i: i for i in list(data_frame.columns)}

    entities = []
    for rowiter in data_frame.iterrows():
        row = rowiter[1]
        entity = cls()
        for attr in get_attribute_dict(entity):
            df_column_name = attr
            if attr in column_name_map:
                df_column_name = column_name_map[attr]
            if df_column_name in row:
                val = row[df_column_name]
                if isinstance(val, pd.Timestamp):
                    val = val.to_pydatetime()
                elif isinstance(val, float):
                    if np.isnan(val):
                        val = None
                setattr(entity, attr, val)
        entities.append(entity)
    return entities


def cast_to_datetime(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to datetime.
    """
    data_frame[column_name] = pd.to_datetime(data_frame[column_name])
    return data_frame


def cast_to_int(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to int.
    """
    return data_frame.astype({column_name: int})


def cast_to_long(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to long(np.int64).
    """
    return data_frame.astype({column_name: np.int64})


def cast_to_short(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to short(np.int16).
    """
    return data_frame.astype({column_name: np.int16})


def cast_to_double(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to double(np.float64).
    """
    return data_frame.astype({column_name: np.float64})


def cast_to_float(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to float(np.float32).
    """
    return data_frame.astype({column_name: np.float32})


def cast_to_string(data_frame: pd.DataFrame, column_name: str):
    """
    Casts given column of dataframe to string.
    """
    data_frame[column_name] = [i if i is None else str(i) for i in data_frame[column_name]]
    return data_frame


def get_column_native_type(data_frame: pd.DataFrame, col: str):
    """Returns ColumnNativeType for given pandas DataFrame column"""
    dtype = data_frame.dtypes[col]
    return get_native_type_from_dtype(dtype)


def get_native_type_from_dtype(dtype):
    """Returns ColumnNativeType for given dtype"""
    if is_string_dtype(dtype):
        return ColumnNativeType.String
    if is_numeric_dtype(dtype):
        return ColumnNativeType.Numeric
    if is_datetime64_any_dtype(dtype):
        return ColumnNativeType.Date
    return ColumnNativeType.Other


def get_numerical_column_names(data_frame: pd.DataFrame) -> List[str]:
    """Returns numerical columns in frame"""
    return [col for col in data_frame.columns if get_column_native_type(data_frame, col) == ColumnNativeType.Numeric]


def get_correlation_matrix_memory_efficient(data_frame: pd.DataFrame, columns: List = None,
                                            n_threads: int = None, only_half_filled: bool = False,
                                            diagonal_values: float = 1.0) -> pd.DataFrame:
    """
    Generate correlation matrix for given frame

    :param List[str] columns: If given, only correlations of given columns will be calculated
    :param int n_threads: Number of threads to use on parallel correlation calculation.
        You can reduce this to reduce memory usage, but execution time will increase.
    :param bool only_half_filled: Only top triangle of the correlation matrix is filled
    :param float diagonal_values: Correlations for same column pairs will be filled with this value
    """
    columns = data_frame.columns.tolist() if columns is None else columns
    num_cols = len(columns)
    corr_matrix = np.empty((num_cols, num_cols))
    corr_matrix.fill(np.nan)
    col_pairs = [(i, j) for i in range(num_cols) for j in range(i, num_cols)]

    def calc_corr_and_fill_matrix(col1, col2):
        if col1 == col2:
            if only_half_filled:
                return
            correlation = diagonal_values
        else:
            correlation = np.corrcoef(data_frame[columns[col1]], data_frame[columns[col2]])[0][1]
        corr_matrix[col1][col2] = correlation
        if not only_half_filled:
            corr_matrix[col2][col1] = correlation

    if n_threads is not None:
        parallel_execution_helper.execute_parallel(col_pairs,
                                                   calc_corr_and_fill_matrix, num_jobs=n_threads,
                                                   require_shared_memory=True)
    else:
        parallel_execution_helper.execute_parallel(col_pairs,
                                                   calc_corr_and_fill_matrix, require_shared_memory=True)
    return pd.DataFrame(corr_matrix, columns=columns).set_index(pd.Index(columns))
