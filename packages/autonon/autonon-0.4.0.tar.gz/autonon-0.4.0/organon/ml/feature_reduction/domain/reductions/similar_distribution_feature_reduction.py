""" This module includes SimilarDistributionFeatureReduction"""
from typing import List, Dict, Tuple, Optional

import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.helpers.univariate_performance_helper import \
    get_reduced_columns_via_performance
from organon.ml.feature_reduction.domain.objects.numeric_column_stats import NumericColumnStats
from organon.ml.feature_reduction.domain.objects.similar_dist_reduction_output import SimilarDistReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.similar_distribution_feature_reduction_settings import \
    SimilarDistributionFeatureReductionSettings


class SimilarDistributionFeatureReduction(BaseFeatureReduction):
    """SimilarDistributionFeatureReduction class"""

    def _execute_reduction(self, settings: SimilarDistributionFeatureReductionSettings) -> SimilarDistReductionOutput:
        data = settings.data
        output = SimilarDistReductionOutput()
        output.feature_reduction_type = FeatureReductionType.SIMILAR_DISTRIBUTION
        included_columns = self._get_included_columns(data, settings.excluded_columns)
        numeric_columns = [col for col in included_columns if
                           (get_column_native_type(data, col) == ColumnNativeType.Numeric)
                           and (col != settings.target_column_name)
                           and (data[col].nunique() > settings.nunique_count)]
        if not numeric_columns:
            output.reduced_column_list = None
            return output
        numeric_columns_stats = self._get_stats(data, numeric_columns)
        similar_distribution_columns = self._get_similar_distribution_columns(numeric_columns_stats)
        reduced_columns, new_col_performances = self._find_reduced_columns(settings, similar_distribution_columns)
        output.reduced_column_list = reduced_columns
        output.new_univariate_performance_results = new_col_performances
        return output

    @staticmethod
    def _get_stats(data: pd.DataFrame, numeric_columns: List[str]) -> List[NumericColumnStats]:
        """
        Return numeric column stats which includes mean,std, percentile 25, percentile 50, percentile 75.
        Parameters
        ----------
        data
        numeric_columns

        Returns
        -------
        Return numeric columns stats list
        """

        stats_df = data[numeric_columns].describe()
        numeric_columns_stats = []
        for col in numeric_columns:
            numeric_column_stats = NumericColumnStats(col, stats_df[col]["mean"], stats_df[col]["std"],
                                                      stats_df[col]["25%"],
                                                      stats_df[col]["50%"],
                                                      stats_df[col]["75%"])
            numeric_columns_stats.append(numeric_column_stats)
        return numeric_columns_stats

    @staticmethod
    def _get_similar_distribution_columns(numeric_columns_stats: List[NumericColumnStats]) -> Dict[str, List[str]]:
        """
        Finds columns with similar distribution using numerical column statistics.        Parameters
        ----------
        numeric_columns_stats

        Returns
        -------
        Returns columns with the same distribution.
        """
        similar_distribution_columns = {}

        similar_distribution_columns_set = set()
        for count, value in enumerate(numeric_columns_stats):
            if value.column_name in similar_distribution_columns_set:
                continue
            column_list = []
            column_list.append(numeric_columns_stats[count].column_name)
            for j in range(count + 1, len(numeric_columns_stats)):

                if numeric_columns_stats[count] == numeric_columns_stats[j]:
                    column_list.append(numeric_columns_stats[j].column_name)
                    similar_distribution_columns_set.add(numeric_columns_stats[j].column_name)
            if len(column_list) > 1:
                similar_distribution_columns[numeric_columns_stats[count].column_name] = column_list
        return similar_distribution_columns

    @staticmethod
    def _find_reduced_columns(settings: SimilarDistributionFeatureReductionSettings,
                              similar_distribution_columns: Dict[str, List[str]]) -> \
            Tuple[List[str], Optional[Dict[str, float]]]:
        """
        Find reduced columns.
        Parameters
        ----------
        settings
        similar_distribution_columns
        numeric_columns_list

        Returns
        -------
        Returns columns list which reduced.
        """
        if len(similar_distribution_columns) == 0:
            return [], None
        reduced_columns = []
        if settings.target_column_name is not None and settings.target_type is not None:
            reduced_columns, new_col_performances = get_reduced_columns_via_performance(
                settings.data, settings.target_column_name, settings.target_type, settings.performance_metric,
                list(similar_distribution_columns.values()), settings.univariate_performance_result,
                random_state=settings.random_state)
            return reduced_columns, new_col_performances

        for column_list in similar_distribution_columns.values():
            column_list.sort()
            reduced_columns.extend(column_list[1:])
        return reduced_columns, None

    def get_description(self) -> str:
        return "Similar Distribution Feature Reduction"
