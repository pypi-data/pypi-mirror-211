""" This module includes HighCorrelatedFeatureReduction"""
import random
from typing import List, Tuple, Optional, Dict

import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.helpers.univariate_performance_helper import \
    get_univariate_performances_for_columns
from organon.ml.feature_reduction.domain.objects.high_corr_reduction_output import HighCorrReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.high_correlated_feature_reduction_settings import \
    HighCorrelatedFeatureReductionSettings


class HighCorrelatedFeatureReduction(BaseFeatureReduction):
    """HighCorrelatedFeatureReduction class"""

    def _execute_reduction(self, settings: HighCorrelatedFeatureReductionSettings) -> HighCorrReductionOutput:
        data = settings.data
        output = HighCorrReductionOutput()
        output.feature_reduction_type = FeatureReductionType.HIGH_CORRELATION

        included_columns = self._get_included_columns(data, settings.excluded_columns)

        numeric_columns = [col for col in included_columns if
                           (get_column_native_type(data, col) == ColumnNativeType.Numeric)
                           and (col != settings.target_column_name)]
        if not numeric_columns:
            output.reduced_column_list = None
            return output
        high_correlated_column_pair = self._get_high_correlated_columns(data, numeric_columns,
                                                                        settings.correlation_threshold)
        reduced_columns, new_col_performances = self._find_reduced_columns(settings, high_correlated_column_pair)
        output.reduced_column_list = reduced_columns
        output.new_univariate_performance_results = new_col_performances
        return output

    @staticmethod
    def _get_high_correlated_columns(data: pd.DataFrame, numeric_columns: List[str],
                                     correlation_threshold: float) -> List[Tuple[str, str]]:
        """
        Find high correlated numeric features
        Parameters
        ----------
        data
        numeric_columns
        correlation_threshold

        Returns
        -------

        """
        column_pairs = []

        corr_matrix = data[numeric_columns].corr(method="spearman").abs()
        corr_matrix_sorted = corr_matrix[corr_matrix > correlation_threshold].unstack().sort_values(
            ascending=False).dropna()

        for col_x, col_y in corr_matrix_sorted.keys():
            if col_x != col_y and col_x < col_y:
                column_pairs.append((col_x, col_y))

        return column_pairs

    def _find_reduced_columns(self, settings: HighCorrelatedFeatureReductionSettings,
                              high_correlated_column_pair: List[Tuple[str, str]]) \
            -> Tuple[List[str], Optional[Dict[str, float]]]:
        """
        Find reduced columns.
        Parameters
        ----------
        settings
        high_correlated_column_pair


        Returns
        -------
        Returns columns list which reduced.
        """
        if len(high_correlated_column_pair) == 0:
            return [], None
        reduced_columns = []

        if settings.target_column_name is not None and settings.target_type is not None:
            reduced_columns, new_performances = self._get_reduced_columns_via_performance(settings,
                                                                                          high_correlated_column_pair)
            return reduced_columns, new_performances
        to_protect = []
        for column_pair in high_correlated_column_pair:
            value = random.sample(list([column_pair[0], column_pair[1]]), 2)
            column_to_drop = value[0]
            if (column_to_drop not in reduced_columns) and (column_to_drop not in to_protect) and (
                    value[1] not in reduced_columns):
                reduced_columns.append(column_to_drop)
                if value[1] not in to_protect:
                    to_protect.append(value[1])

        return reduced_columns, None

    @staticmethod
    def _get_reduced_columns_via_performance(
            settings: HighCorrelatedFeatureReductionSettings,
            high_correlated_columns_info: List[Tuple[str, str]]) -> Tuple[List[str], Optional[Dict[str, float]]]:
        """
        Finds the reduced column using the univariate performance result.
        Parameters
        ----------
        settings
        high_correlated_columns_info

        Returns
        -------
        Returns columns list which reduced.

        """

        data = settings.data
        target_type = settings.target_type
        target_column_name = settings.target_column_name
        existing_performances = {} if settings.univariate_performance_result is None \
            else settings.univariate_performance_result
        new_performances = {}

        to_protect = []
        reduced_columns = []
        for column_pair in high_correlated_columns_info:
            if column_pair[0] in to_protect and column_pair[1] in to_protect:
                continue
            score_result = {}
            for column in column_pair:
                if column not in existing_performances:
                    column_perf = get_univariate_performances_for_columns(
                        data, [column], target_column_name, target_type, settings.performance_metric,
                        settings.random_state)[column]
                    new_performances[column] = column_perf
                    score_result[column] = column_perf
                else:
                    score_result[column] = existing_performances[column]
            best_score_column = max(score_result, key=score_result.get)
            for column in column_pair:
                if column != best_score_column:
                    if (column not in reduced_columns) and (column not in to_protect):
                        reduced_columns.append(column)
                elif column not in to_protect:
                    to_protect.append(column)

        return reduced_columns, new_performances

    def get_description(self) -> str:
        return "High Correlated Feature Reduction"
