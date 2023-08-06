"""Includes FeatureSimilaritySelectionService class."""
from typing import List

import numpy as np
import pandas as pd

from organon.fl.core.helpers.data_frame_helper import get_correlation_matrix_memory_efficient
from organon.fl.mathematics.constants import DOUBLE_MAX
from organon.ml.feature_selection.domain.objects.feature_similarity_selection_output import \
    FeatureSimilaritySelectionOutput
from organon.ml.feature_selection.domain.objects.settings.feature_similarity_selection_settings import \
    FeatureSimilaritySelectionSettings
from organon.ml.feature_selection.domain.services.base_feature_selection_service import SelectionRunSettings
from organon.ml.feature_selection.domain.services.base_unsupervised_feature_selection_service import \
    BaseUnsupervisedFeatureSelectionService


class FeatureSimilaritySelectionService(BaseUnsupervisedFeatureSelectionService[FeatureSimilaritySelectionSettings,
                                                                                FeatureSimilaritySelectionOutput]):
    """Service class for Feature Similarity selection"""

    @classmethod
    def _validate_settings(cls, settings: FeatureSimilaritySelectionSettings):
        pass

    @classmethod
    def _run(cls, run_settings: SelectionRunSettings) -> FeatureSimilaritySelectionOutput:
        settings: FeatureSimilaritySelectionSettings = run_settings.settings
        data_frame = run_settings.data
        output = FeatureSimilaritySelectionOutput()
        variances = cls._get_column_variances(data_frame)
        zero_variance_cols = list((variances[variances == 0]).index)
        nan_max_cols = [col for col in data_frame if np.isnan(data_frame[col].max())]
        dropped_columns = set(zero_variance_cols + nan_max_cols)
        col_list = data_frame.columns.difference(dropped_columns).to_list()
        if len(col_list) <= 1:
            output.selected_features = col_list
            return output

        mci_df = cls.__get_corr_df(data_frame, variances, col_list, settings.prioritize_performance)

        k_val = round(len(mci_df.columns) * settings.selection_percent)
        if k_val > mci_df.shape[0] - 1:
            k_val = mci_df.shape[0] - 1

        if k_val > 1:
            min_rik = cls.__get_min_rik_and_update_corr_df(mci_df, k_val)
            eps = min_rik
            while True:
                if k_val > mci_df.shape[0] - 1:
                    k_val = mci_df.shape[0] - 1
                if k_val <= 1:
                    break
                k_val = k_val - 1
                min_rik = cls.__get_min_rik_and_update_corr_df(mci_df, k_val)
                if np.isnan(min_rik) or min_rik <= eps:
                    break

        selected_set = mci_df.columns
        output.selected_features = list(selected_set)
        return output

    @classmethod
    def _get_column_variances(cls, data_frame: pd.DataFrame):
        # calculate variances column by column for memory efficiency
        variances = []
        for col in data_frame:
            variances.append(data_frame[col].var())
        return pd.Series(variances, index=data_frame.columns)

    @classmethod
    def __get_min_rik_and_update_corr_df(cls, mci_df: pd.DataFrame, k_val: int):
        min_rik_feature, min_rik = cls.__find_min_rik(mci_df, k_val)
        discard_list = list(mci_df[min_rik_feature].sort_values().index)[:k_val]
        mci_df.drop(discard_list, axis=1, inplace=True)
        mci_df.drop(discard_list, axis=0, inplace=True)
        return min_rik

    @classmethod
    def __find_min_rik(cls, mci_df: pd.DataFrame, k_val: int):
        min_rik_feature = None
        min_rik = DOUBLE_MAX
        for col in mci_df.columns:
            kth_col = list(mci_df[col].sort_values().index)[k_val - 1]
            rik = mci_df.loc[col, kth_col]
            if rik < min_rik:
                min_rik_feature = col
                min_rik = rik
        return min_rik_feature, min_rik

    @classmethod
    def __get_corr_df(cls, data_frame: pd.DataFrame, variances: pd.Series, col_list: List[str],
                      prioritize_performance: bool):
        mci_df = cls._get_correlation_matrix(data_frame, col_list, prioritize_performance)
        same_drop_cols = set()
        for col1_index, col1 in enumerate(col_list):
            mci_df.loc[col1, col1] = np.nan
            if col1_index == len(col_list):
                break
            var1 = variances[col1]
            other_cols = col_list[col1_index + 1:]
            new_vals = []
            for col2 in other_cols:
                corr = mci_df.loc[col1, col2]
                var2 = variances[col2]
                mci = 0.5 * (var1 + var2 - np.sqrt(
                    np.square((var1 + var2)) - 4 * var1 * var2 * (1 - np.square(corr))))
                new_vals.append(mci)
                if mci == 0:
                    same_drop_cols.add(col2)
            mci_df.loc[col1, other_cols] = new_vals
            mci_df.loc[other_cols, col1] = new_vals
        mci_df.drop(same_drop_cols, axis=1, inplace=True)
        mci_df.drop(same_drop_cols, axis=0, inplace=True)

        drop_list = list(mci_df[mci_df.max().isnull()].index)
        mci_df.drop(drop_list, axis=1, inplace=True)
        mci_df.drop(drop_list, axis=0, inplace=True)
        return mci_df

    @classmethod
    def _get_correlation_matrix(cls, data: pd.DataFrame, col_list: List[str], prioritize_performance: bool):
        if prioritize_performance:
            return data.corr().loc[col_list, col_list]
        return get_correlation_matrix_memory_efficient(data, columns=col_list)
