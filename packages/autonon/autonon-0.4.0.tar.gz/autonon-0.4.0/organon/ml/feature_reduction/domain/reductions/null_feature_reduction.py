""" This module includes NullFeatureReduction"""
from typing import List

import pandas as pd

from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.null_feature_reduction_settings import NullFeatureReductionSettings


class NullFeatureReduction(BaseFeatureReduction):
    """ NullFeatureReduction class"""

    def _execute_reduction(self, settings: NullFeatureReductionSettings) -> FeatureReductionOutput:
        output = FeatureReductionOutput()
        included_columns = self._get_included_columns(settings.data, settings.excluded_columns)
        missing_df = self._calculate_null_ratio(settings.data, included_columns)
        output.feature_reduction_type = FeatureReductionType.NULL

        if missing_df is None:
            output.reduced_column_list = None
            return output

        reduced_columns = self._find_reduced_columns(missing_df, settings.null_ratio_threshold)
        output.reduced_column_list = reduced_columns
        return output

    @staticmethod
    def _calculate_null_ratio(data: pd.DataFrame, included_columns: List[str] = None):

        if not included_columns:
            return None

        na_columns = [col for col in included_columns if data[col].isnull().sum() > 0]

        ratio = (data[na_columns].isnull().sum() / data.shape[0])
        missing_df = pd.DataFrame(ratio)
        missing_df.reset_index(inplace=True)
        missing_df.columns = ["columns", "ratio"]
        return missing_df

    @staticmethod
    def _find_reduced_columns(missing_df: pd.DataFrame, null_ratio_threshold: float) -> List[str]:
        reduced_columns = [col for col in missing_df["columns"] if (missing_df[missing_df["columns"] == col]["ratio"]
                                                                    > null_ratio_threshold).any(axis=None)]
        return reduced_columns

    def get_description(self) -> str:
        return "Null Feature Reduction"
