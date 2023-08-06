"""Includes ImputationService class."""
from typing import List, Union, Dict, Type

import numpy as np
import pandas as pd
# this import must stay: https://github.com/scikit-learn/scikit-learn/issues/16833
# noinspection PyUnresolvedReferences
from sklearn.experimental import enable_iterative_imputer  # pylint: disable=unused-import
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.common.helpers.parameter_helper import get_params
from organon.ml.preprocessing.domain.objects.imputation_fit_output import ImputationFitOutput
from organon.ml.preprocessing.settings.enums.imputer_type import ImputerType
from organon.ml.preprocessing.settings.objects.imputation_settings import ImputationSettings


class ImputationService:
    """Service for null value imputation"""

    def __init__(self, settings: ImputationSettings):
        self.settings = settings
        self.fit_output: ImputationFitOutput = None
        self.numerical_col_list: List[str] = None
        self.categorical_col_list: List[str] = None

    def fit(self, data: pd.DataFrame) -> ImputationFitOutput:
        """Fits train data by categorical and numeric imputers based on whether a col is numeric or not"""
        if data is None or data.empty:
            raise ValueError("Imputer cannot be fit. Data is not provided.")
        if self.settings.categorical_data_method == ImputerType.ITERATIVE:
            raise ValueError("IterativeImputer cannot be used for categorical columns")
        self._fill_column_lists(data)
        fit_output = ImputationFitOutput()
        fit_output.numerical_imputer = {}
        fit_output.categorical_imputer = {}
        categorical_imputer = self._get_imputer(self.settings.categorical_data_method)
        categorical_imputer_params = self._get_params(self.settings.categorical_data_method,
                                                      self.settings.c_strategy, self.settings.c_missing_values,
                                                      self.settings.c_fill_value)
        for col in self.categorical_col_list:
            imputer = categorical_imputer(**categorical_imputer_params)
            imputer.fit(data[[col]])
            fit_output.categorical_imputer[col] = imputer
        numerical_imputer = self._get_imputer(self.settings.numeric_data_method)
        numerical_imputer_params = self._get_params(self.settings.numeric_data_method, self.settings.n_strategy,
                                                    self.settings.n_missing_values, self.settings.n_fill_value)

        if self.settings.numeric_data_method == ImputerType.SIMPLE:
            for col in self.numerical_col_list:
                imputer = numerical_imputer(**numerical_imputer_params)
                imputer.fit(data[[col]])
                fit_output.numerical_imputer[col] = imputer
        else:
            imputer = numerical_imputer(**numerical_imputer_params)
            imputer.fit(data[self.numerical_col_list])
            fit_output.numerical_imputer = imputer
        self.fit_output = fit_output
        return fit_output

    @staticmethod
    def _get_imputer(imputing_method: ImputerType) -> Union[Type[SimpleImputer], Type[IterativeImputer]]:
        if imputing_method is ImputerType.SIMPLE:
            return SimpleImputer
        return IterativeImputer

    @staticmethod
    def _get_params(imputing_method: ImputerType, strategy: str,
                    missing_values: Union[int, float, str, None],
                    fill_value: Union[float, str, int]) -> Dict:
        if imputing_method is ImputerType.SIMPLE:
            return get_params({"strategy": strategy, "missing_values": missing_values, "fill_value": fill_value})
        return get_params({"initial_strategy": strategy, "missing_values": missing_values})

    def transform(self, data: pd.DataFrame, inplace: bool = False,
                  ignore_extra_columns: bool = False) -> pd.DataFrame:
        """Fills missing values in data and return it."""
        if self.fit_output is None:
            raise ValueError("Imputer not fitted yet. Run fit method first.")

        self._validate_transformation_data(data, ignore_extra_columns)

        if not inplace:
            trans_data = data.copy()
        else:
            trans_data = data
        categorical_col_list = [col for col in trans_data.columns if col in self.categorical_col_list]
        numerical_col_list = [col for col in trans_data.columns if col in self.numerical_col_list]

        for col in categorical_col_list:
            self._try_set_col_after_transform(trans_data, col, self.fit_output.categorical_imputer[col])
        if isinstance(self.fit_output.numerical_imputer, IterativeImputer):
            trans_data[self.numerical_col_list] = self.fit_output.numerical_imputer.transform(
                trans_data[self.numerical_col_list])
        else:
            for col in numerical_col_list:
                self._try_set_col_after_transform(trans_data, col, self.fit_output.numerical_imputer[col])
        return trans_data

    def _validate_transformation_data(self, trans_data: pd.DataFrame, ignore_extra_columns: bool):
        self._check_extra_columns_in_transformation_data(trans_data, ignore_extra_columns)

        if isinstance(self.fit_output.numerical_imputer, IterativeImputer):
            missing_cols = [col for col in self.numerical_col_list if col not in trans_data.columns]
            if missing_cols:
                raise ValueError(f"Following numerical columns should be supplied to transform data: "
                                 f"{self._get_list_str(missing_cols)}")

        self._check_changed_type_columns(trans_data)

    def _check_extra_columns_in_transformation_data(self, trans_data: pd.DataFrame, ignore_extra_columns: bool):
        train_cols = self.numerical_col_list + self.categorical_col_list
        if not ignore_extra_columns:
            different_columns = [col for col in trans_data.columns if col not in train_cols]
            if different_columns:
                raise ValueError(f"Imputer was not fitted for following columns: "
                                 f"{self._get_list_str(different_columns)}. "
                                 "Set 'ignore_extra_columns=True' if you want to transform only columns fitted "
                                 "and ignore others")

    def _check_changed_type_columns(self, trans_data: pd.DataFrame):
        numerical_changed_type_cols = []
        for col in self.numerical_col_list:
            if col in trans_data.columns:
                if get_column_native_type(trans_data, col) != ColumnNativeType.Numeric:
                    numerical_changed_type_cols.append(col)
        if numerical_changed_type_cols:
            raise ValueError(
                f"Following columns are expected to be numerical: {self._get_list_str(numerical_changed_type_cols)}")
        categorical_changed_type_cols = []
        for col in self.categorical_col_list:
            if col in trans_data.columns:
                if get_column_native_type(trans_data, col) != ColumnNativeType.String:
                    categorical_changed_type_cols.append(col)
        if categorical_changed_type_cols:
            raise ValueError(
                f"Following columns are expected to be categorical: "
                f"{self._get_list_str(categorical_changed_type_cols)}")

    @classmethod
    def _try_set_col_after_transform(cls, trans_data: pd.DataFrame, col: str, imputer):
        initial_dtype = trans_data[col].dtype
        transformed_arr = imputer.transform(trans_data[[col]])
        if transformed_arr.shape[1] != 0:
            trans_data[col] = transformed_arr
            if trans_data[col].dtype == np.dtype("O"):
                # 'imputer.transform' can convert types like Int64DType to object. Here we try to convert it to
                try:
                    trans_data[col] = trans_data[col].astype(initial_dtype)
                except:  # pylint: disable=bare-except
                    trans_data[col] = trans_data[col].convert_dtypes()
        else:
            if trans_data[col].isna().all():
                LogHelper.warning(f"Column {col} could not be transformed by imputer since all values are NaN.")

    def _fill_column_lists(self, data: pd.DataFrame):
        self.numerical_col_list = []
        self.categorical_col_list = []
        if self.settings.included_columns is None:
            columns = data.columns
        else:
            columns = self.settings.included_columns
        for col in columns:
            col_type = get_column_native_type(data, col)
            if col_type == ColumnNativeType.String:
                self.categorical_col_list.append(col)
            elif col_type == ColumnNativeType.Numeric:
                self.numerical_col_list.append(col)

    @staticmethod
    def _get_list_str(_list: list):
        return ",".join(_list)
