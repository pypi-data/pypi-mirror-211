"""Includes OneHotEncodingService class"""
from typing import List, Dict, Optional

import numpy as np
import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.mathematics.constants import INT_MAX
from organon.ml.preprocessing.settings.objects.one_hot_encoding_settings import OneHotEncodingSettings


class OneHotEncodingService:
    """Service for one hot encoding"""

    NULLS_COL_KEY = "_$NullValue$_"
    OTHERS_COL_KEY = "_$OtherValues$_"

    def __init__(self, settings: OneHotEncodingSettings):
        self._settings = settings
        self._categorical_cols = None
        self._features_dict: Dict[str, List[str]] = None
        self._columns_dict: Dict[str, List[str]] = None
        self._all_ohe_columns: Dict[str, Dict[str, str]] = None

    @property
    def features_dict(self):
        """Returns selected features per categorical column"""
        return self._features_dict

    @property
    def columns_dict(self):
        """Returns generated columns per categorical columns (after transform)"""
        return self._columns_dict

    def fit(self, data: pd.DataFrame):
        """Fit encoder"""
        if self._settings.threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if self._settings.max_bin < 0:
            raise ValueError("Maximum number of features cannot be negative.")
        if data is None or data.empty:
            raise ValueError("Train data cannot be null or empty.")
        self._categorical_cols = [col for col in data if get_column_native_type(data, col) == ColumnNativeType.String]
        self._features_dict = {}
        for col in self._categorical_cols:
            self._features_dict[col] = self._get_col_features(data, col, self._settings.threshold,
                                                              self._settings.max_bin)
        return self

    def transform(self, data: pd.DataFrame, inplace: bool = False):
        """Transform data"""
        if self._features_dict is None:
            raise ValueError("Encoder not fitted yet")
        if data is None or data.empty:
            raise ValueError("Transformation data cannot be null or empty.")
        if not inplace:
            trans_data = data.copy()
        else:
            trans_data = data
        different_columns = [col for col in trans_data if
                             (get_column_native_type(trans_data, col) == ColumnNativeType.String and
                              col not in self._categorical_cols)]
        if different_columns:
            raise ValueError(
                f"These columns are not found in the train data or"
                f" their types were not categorical: {', '.join(different_columns)}.")

        generated_cols_per_category = {}
        all_ohe_col_names_dict = {}
        all_ohe_columns = []
        data_cols = trans_data.columns.tolist()
        for col in self._categorical_cols:
            features = self._features_dict[col]
            new_col_names_dict = self._get_all_new_column_names(data_cols + all_ohe_columns, col, features)
            new_col_names = list(new_col_names_dict.values())
            all_ohe_columns.extend(new_col_names)
            generated_cols_per_category[col] = new_col_names
            all_ohe_col_names_dict[col] = new_col_names_dict
        self._all_ohe_columns = all_ohe_col_names_dict
        self._columns_dict = generated_cols_per_category

        trans_data.loc[:, all_ohe_columns] = np.uint8(0)
        for col in self._categorical_cols:
            features = self._features_dict[col]
            self._set_ohe_column_values(trans_data, col, features, all_ohe_col_names_dict[col])
            del trans_data[col]
        return trans_data

    def get_ohe_col_name_for_categorical_value(self, original_col_name: str, value: str) -> Optional[str]:
        """Returns name of the generated OHE column for given categorical value.
        Returns None if no special OHE column was generated for given value."""
        self._check_transformed()
        if original_col_name not in self._all_ohe_columns:
            raise ValueError(f"No OHE column was generated for column {original_col_name}")
        if pd.isna(value):
            raise ValueError("Value is NA. Use get_ohe_col_name_for_nulls "
                             "if you meant to get column names for NA values.")
        if value in self._all_ohe_columns[original_col_name]:
            return self._all_ohe_columns[original_col_name][value]
        return None

    def get_ohe_col_name_for_nulls(self, original_col_name: str) -> Optional[str]:
        """Returns name of the generated OHE column for NULLs category.
        Returns None if no special OHE column was generated for NULL values."""
        self._check_transformed()
        if original_col_name not in self._all_ohe_columns:
            raise ValueError(f"No OHE column was generated for column {original_col_name}")
        if OneHotEncodingService.NULLS_COL_KEY not in self._all_ohe_columns[original_col_name]:
            return None
        return self._all_ohe_columns[original_col_name][OneHotEncodingService.NULLS_COL_KEY]

    def get_ohe_col_name_for_others(self, original_col_name: str) -> Optional[str]:
        """Returns name of the generated OHE column for Others category.
        Returns None if no special OHE column was generated for extra values."""
        self._check_transformed()
        if original_col_name not in self._all_ohe_columns:
            raise ValueError(f"No OHE column was generated for column {original_col_name}")
        if OneHotEncodingService.OTHERS_COL_KEY not in self._all_ohe_columns[original_col_name]:
            return None
        return self._all_ohe_columns[original_col_name][OneHotEncodingService.OTHERS_COL_KEY]

    def _check_transformed(self):
        if self._all_ohe_columns is None:
            raise ValueError("transform not called yet")

    @staticmethod
    def _get_col_features(data: pd.DataFrame, col: str, threshold: float, max_bin: int) -> List:
        col_params_df = data[col].value_counts(dropna=False)
        col_params_df = col_params_df.reset_index(level=0)
        col_params_df.columns = ["category", "value"]
        col_params_df["percentage"] = col_params_df["value"] / len(data)
        col_params_df["percentage"] = col_params_df["percentage"].cumsum(axis=0)
        number_of_features = OneHotEncodingService._calc_number_of_features(data, col_params_df, threshold, max_bin)
        return col_params_df.iloc[:number_of_features]["category"].to_list()

    @staticmethod
    def _calc_number_of_features(data: pd.DataFrame, col_params: pd.DataFrame, threshold: float, max_bin: int):
        if threshold == 1.0:
            return min(len(data), max_bin)
        if max_bin == INT_MAX:
            return col_params[col_params["percentage"] >= threshold].index[0] + 1
        return min(col_params[col_params["percentage"] >= threshold].index[0] + 1, max_bin)

    @staticmethod
    def _get_all_new_column_names(current_columns_in_frame: List[str], col: str, features: List) -> Dict[str, str]:
        generated_cols = {}
        columns_in_frame = current_columns_in_frame.copy()
        for feature in features:
            if pd.isna(feature):
                col_name = OneHotEncodingService._decide_col_name(columns_in_frame,
                                                                  OneHotEncodingService._get_nulls_col_name(col))
                generated_cols["_$NullValue$_"] = col_name
            else:
                col_name = OneHotEncodingService._decide_col_name(columns_in_frame,
                                                                  OneHotEncodingService._get_feature_col_name(col,
                                                                                                              feature))
                generated_cols[feature] = col_name

            columns_in_frame.append(col_name)

        others_col = OneHotEncodingService._decide_col_name(columns_in_frame,
                                                            OneHotEncodingService._get_others_col_name(col))
        generated_cols["_$OtherValues$_"] = others_col
        return generated_cols

    @staticmethod
    def _decide_col_name(current_columns_in_frame: List[str], col: str) -> str:
        name_index = 2
        col_name = col
        while col_name in current_columns_in_frame:
            col_name = f"{col}{name_index}"
            name_index += 1
        return col_name

    @staticmethod
    def _get_others_col_name(col: str):
        # two underscores used. This makes sure no name collision will occur with other feature columns
        return f"{col}__OTHER"

    @staticmethod
    def _get_nulls_col_name(col: str):
        # two underscores used. This makes sure no name collision will occur with other feature columns
        return f"{col}__NULL"

    @staticmethod
    def _get_feature_col_name(col: str, feature):
        return f"{col}___{feature}"

    @staticmethod
    def _set_ohe_column_values(data: pd.DataFrame, col: str, features: List, ohe_col_names: Dict[str, str]):
        for feature in features:
            if pd.isna(feature):
                transformed_col_name = ohe_col_names[OneHotEncodingService.NULLS_COL_KEY]
                data[transformed_col_name] = np.where(pd.isna(data[col]), 1, 0).astype(np.uint8)
            else:
                transformed_col_name = ohe_col_names[feature]
                data[transformed_col_name] = np.where(data[col] == feature, 1, 0).astype(np.uint8)
        others_col_name = ohe_col_names[OneHotEncodingService.OTHERS_COL_KEY]
        data[others_col_name] = np.where(data[col].isin(features), 0, 1).astype(np.uint8)
