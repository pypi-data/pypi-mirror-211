"""Includes helper functions for target-trx source reading"""
import pandas as pd
from pandas.core.dtypes.common import is_string_dtype, is_integer_dtype


def validate_entity_column(source_name: str, data_frame: pd.DataFrame, entity_col_name: str):
    """Validates entity column - used for both trx and target frame"""
    if not is_string_dtype(data_frame.dtypes[entity_col_name]) and not is_integer_dtype(
            data_frame.dtypes[entity_col_name]):
        raise ValueError(f"{source_name} data entity column type should be either integer or string")
