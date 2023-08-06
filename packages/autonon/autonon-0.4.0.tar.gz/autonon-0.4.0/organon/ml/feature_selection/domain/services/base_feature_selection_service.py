"""Includes BaseFeatureSelectionService class."""
import abc
from typing import TypeVar, Generic, Dict, List

import numpy as np
import pandas as pd

from organon.fl.core.helpers.data_frame_helper import get_numerical_column_names
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.feature_selection.domain.objects.base_selection_output import BaseSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.base_feature_selection_settings import \
    BaseFeatureSelectionSettings
from organon.fl.modelling.unsupervised_feature_extractor import UnsupervisedFeatureExtractor
from organon.ml.preprocessing.services.preprocessor import Preprocessor
from organon.ml.preprocessing.settings.enums.imputer_type import ImputerType

FeatureSelectionSettingsType = TypeVar("FeatureSelectionSettingsType", bound=BaseFeatureSelectionSettings)
FeatureSelectionOutputType = TypeVar("FeatureSelectionOutputType", bound=BaseSelectionOutput)


class SelectionRunSettings:
    """All settings to run selection after preprocessing"""

    def __init__(self, preprocessed_data: pd.DataFrame, settings,
                 ohe_columns: Dict[str, List[str]]):
        self.data = preprocessed_data
        self.settings = settings
        self.ohe_columns = ohe_columns


class BaseFeatureSelectionService(Generic[FeatureSelectionSettingsType, FeatureSelectionOutputType],
                                  metaclass=abc.ABCMeta):
    """Base service class for feature selection services"""

    def __init__(self):
        self.settings: FeatureSelectionSettingsType = None

    @classmethod
    def run_selection(cls, settings: FeatureSelectionSettingsType) -> FeatureSelectionOutputType:
        """Run selection algorithm and return output with selected features"""
        cls._validate_settings(settings)
        data, ohe_columns = cls._preprocess(settings.data)
        run_settings = SelectionRunSettings(data, settings, ohe_columns)
        output = cls._run(run_settings)
        output.selected_features = cls._get_normalized_selected_features(output.selected_features, ohe_columns)
        return output

    @classmethod
    @abc.abstractmethod
    def _run(cls, run_settings: SelectionRunSettings) -> BaseSelectionOutput:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _validate_settings(cls, settings: FeatureSelectionSettingsType):
        raise NotImplementedError

    @classmethod
    def _preprocess(cls, data: pd.DataFrame):
        numerical_columns = get_numerical_column_names(data)
        columns_with_nan_values = [col for col in numerical_columns if data[col].isnull().values.any()]
        execute_imputation = len(columns_with_nan_values) > 0
        execute_ohe = len(numerical_columns) != len(data.columns)
        ohe_columns_dict = None
        if execute_imputation or execute_ohe:
            data = data.copy()
            if execute_imputation:
                imputation_service = Preprocessor().get_imputation_service(numeric_data_method=ImputerType.SIMPLE.name,
                                                                           n_strategy="median",
                                                                           included_columns=numerical_columns)
                imputation_service.fit(data)
                data = imputation_service.transform(data)
            if execute_ohe:
                ohe_service = Preprocessor.get_one_hot_encoding_service()
                ohe_service.fit(data)
                data = ohe_service.transform(data)
                ohe_columns_dict = ohe_service.columns_dict
        return data, ohe_columns_dict

    @classmethod
    def _get_normalized_selected_features(cls, selected_features: List[str], ohe_columns: Dict[str, List[str]]):
        if ohe_columns is None:
            return selected_features.copy()
        reverse_dict = {}
        for str_col, generated_num_cols in ohe_columns.items():
            for col in generated_num_cols:
                reverse_dict[col] = str_col
        actual_features = set()
        for feature in selected_features:
            if feature in reverse_dict:
                actual_col = reverse_dict[feature]
                actual_features.add(actual_col)
            else:
                actual_features.add(feature)
        return list(actual_features)

    @classmethod
    def _get_features_with_sweep(cls, data: pd.DataFrame, sweep_args: dict):
        sweep_args = {} if sweep_args is None else sweep_args.copy()
        n_threads = 1
        if "n_threads" in sweep_args:
            n_threads = sweep_args.pop("n_threads")
        if "max_col_count" in sweep_args:
            max_col_count = sweep_args.pop("max_col_count")
            sweep_args["max_iter"] = max_col_count
        df_as_dict = cls.__get_df_as_dict_for_sweep(data)
        extractor = UnsupervisedFeatureExtractor(df_as_dict, **sweep_args)
        return extractor.execute(num_threads=n_threads)

    @classmethod
    def __get_df_as_dict_for_sweep(cls, data: pd.DataFrame):
        df_dict = {}
        for col in data.columns:
            if data.dtypes[col].type != np.float32:
                df_dict[col] = data[col].astype(np.float32)
            else:
                df_dict[col] = data[col]
        return df_dict

    @classmethod
    def _validate_original_data_for_sweep(cls, data: pd.DataFrame):
        invalid_cols = []
        for col in get_numerical_column_names(data):
            if data.dtypes[col].type != np.float32:
                invalid_cols.append(col)
        if invalid_cols:
            LogHelper.warning(
                "dtypes of these numeric columns will be converted to np.float32 before sweep: " +
                ",".join(invalid_cols))
