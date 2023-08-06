"""Includes RegressionReporterService class."""
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error, mean_squared_log_error
from sklearn.metrics import r2_score

from organon.ml.common.helpers.df_ops_helper import get_bins
from organon.ml.reporting.domain.objects.regression_report import RegressionReport
from organon.ml.reporting.domain.services.base_reporter_service import BaseReporterService
from organon.ml.reporting.settings.objects.reporter_settings import ReporterSettings


class RegressionReporterService(BaseReporterService[RegressionReport]):
    """Reporter service for regression"""

    def execute(self, settings: ReporterSettings) -> RegressionReport:
        id_str_exists = settings.id_str_column is not None
        split_col_exists = settings.split_column is not None
        group_by_columns = []
        if id_str_exists:
            group_by_columns.append(settings.id_str_column)
        if split_col_exists:
            group_by_columns.append(settings.split_column)

        lift_cols, performance_summary_cols = self._get_lift_and_perf_columns(id_str_exists, split_col_exists)
        if group_by_columns:
            performance_summary_list = []
            lift_list = []
            for groups, indices in settings.data.groupby(group_by_columns).indices.items():
                group_tuple = groups if isinstance(groups, tuple) else (groups,)
                performance_summary_list.append([*list(group_tuple), *self._calc_performance_summary_for_split(
                    settings.data.loc[indices], settings.target_column, settings.score_column).tolist()])
                lift_tables = self._create_lift_table_data(settings.data.loc[indices],
                                                           settings.target_column,
                                                           settings.score_column,
                                                           settings.num_bins)
                for i in range(settings.num_bins):
                    lift_list.append([*list(group_tuple), *lift_tables[i]])
            lift_table = pd.DataFrame(data=lift_list, columns=lift_cols)
            performance_summary_table = pd.DataFrame(data=performance_summary_list, columns=performance_summary_cols)
        else:
            lift_table = pd.DataFrame(data=self._create_lift_table_data(settings.data, settings.target_column,
                                                                        settings.score_column, settings.num_bins),
                                      columns=lift_cols)
            performance_summary_table = pd.DataFrame(data=[self._calc_performance_summary_for_split(
                settings.data, settings.target_column, settings.score_column).values], columns=performance_summary_cols)
        report = RegressionReport()
        report.performance_summary = performance_summary_table
        report.lift_table = lift_table
        return report

    @staticmethod
    def _get_lift_and_perf_columns(idstr_exists=False, split_exists=False) -> Tuple[List, List]:
        lift_columns = ["Bin", "Total Count", "Target Average", "Score Average", "Cumulative Lift"]
        perf_summary_columns = ["MSE", "RMSE", "MAA", "MAPE", "MSLOGE", "R2", "ROW COUNT", "TARGET AVG", "SCORE AVG",
                                "SCORE STD", "SCORE MIN", "SCORE P25", "SCORE MEDIAN", "SCORE P75", "SCORE MAX"]
        if split_exists:
            lift_columns.insert(0, "Data")
            perf_summary_columns.insert(0, "Data")
        if idstr_exists:
            lift_columns.insert(0, "IdStr")
            perf_summary_columns.insert(0, "IdStr")
        return lift_columns, perf_summary_columns

    def _get_empty_lift_perf_tables(self, idstr_exists=False, split_exists=False) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return pd.DataFrame(columns=self._get_lift_and_perf_columns(idstr_exists, split_exists)[0]), \
               pd.DataFrame(columns=self._get_lift_and_perf_columns(idstr_exists, split_exists)[1])

    def _create_lift_table_data(self, split_df: pd.DataFrame, target_column: str,
                                score_column: str, num_bins: int) -> List:
        if num_bins > len(split_df):
            raise ValueError("num_bins cannot be higher than number of rows in a set")
        split_bins = get_bins(split_df[score_column], num_bins)
        return self._get_bin_list(split_df, target_column, split_bins, score_column, num_bins)

    @staticmethod
    def _get_bin_list(data: pd.DataFrame, target_column: str, bins: pd.Series, score_column: str,
                      num_bins: int) -> List:
        bin_list = []
        target_avg = data[target_column].mean()
        cumulative_sum, cumulative_count = 0, 0
        for bin_num in reversed(range(num_bins)):
            data_bins = data.loc[bins == bin_num]
            bin_target_avg = data_bins[target_column].mean()
            bin_length = len(data_bins)
            cumulative_sum += bin_target_avg * bin_length
            cumulative_count += bin_length
            bin_list.append([bin_num, bin_length, bin_target_avg,
                             data_bins[score_column].mean(),
                             cumulative_sum / (cumulative_count * target_avg)])
        bin_list.reverse()
        return bin_list

    def _calc_performance_summary_for_split(self, split_data: pd.DataFrame, target_col: str, prediction_col: str):
        df_statistics = split_data[prediction_col].agg(["mean", "std", "min", "max", "median"])
        percentiles = np.percentile(split_data[prediction_col], [25, 50, 75])
        return pd.Series(data=[mean_squared_error(split_data[target_col], split_data[prediction_col]),
                               mean_squared_error(split_data[target_col], split_data[prediction_col], squared=False),
                               mean_absolute_error(split_data[target_col], split_data[prediction_col]),
                               self._mean_absolute_percentage_error(split_data[target_col], split_data[prediction_col]),
                               mean_squared_log_error(split_data[target_col], split_data[prediction_col]),
                               r2_score(split_data[target_col], split_data[prediction_col]),
                               len(split_data),
                               split_data[target_col].mean(),
                               df_statistics["mean"],
                               df_statistics["std"],
                               df_statistics["min"],
                               percentiles[0],
                               percentiles[1],
                               percentiles[2],
                               df_statistics["max"]]
                         )

    @staticmethod
    def _mean_absolute_percentage_error(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        y_true[y_true == 0] = 1
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
