"""Includes BinaryReporterService class."""
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from organon.ml.common.helpers.df_ops_helper import get_bins
from organon.ml.reporting.domain.objects.binary_report import BinaryReport
from organon.ml.reporting.domain.services.base_reporter_service import BaseReporterService
from organon.ml.reporting.settings.objects.reporter_settings import ReporterSettings


class BinaryReporterService(BaseReporterService[BinaryReport]):
    """Reporter service for binary classification"""

    @classmethod
    def execute(cls, settings: ReporterSettings) -> BinaryReport:
        group_by_columns = []
        id_str_col_exists = settings.id_str_column is not None
        split_col_exists = settings.split_column is not None

        if id_str_col_exists:
            group_by_columns.append(settings.id_str_column)
        if split_col_exists:
            group_by_columns.append(settings.split_column)

        perf_sum_columns = cls.__get_columns_for_performance_summary_df(id_str_col_exists, split_col_exists)
        detailed_perf_sum_columns = cls.__get_columns_for_detailed_performance_summary_df(id_str_col_exists,
                                                                                          split_col_exists)
        target_based_summary_columns = cls.__get_columns_for_target_based_performance_summary_df(id_str_col_exists,
                                                                                                 split_col_exists)
        if group_by_columns:
            performance_summary_dicts = []
            all_bin_performances = []
            all_target_based_performances = []
            for groups, indices in settings.data.groupby(group_by_columns).indices.items():
                group_tuple = groups if isinstance(groups, tuple) else (groups,)
                general_performance_dict_for_group, bin_performances, target_based_score_perf = \
                    cls.__get_details(settings, settings.data.loc[indices])
                cls.__add_group_values_to_dict(general_performance_dict_for_group, group_tuple, id_str_col_exists,
                                               split_col_exists)
                cls.__add_group_values_to_dict(target_based_score_perf, group_tuple, id_str_col_exists,
                                               split_col_exists)
                for _dict in bin_performances:
                    cls.__add_group_values_to_dict(_dict, group_tuple, id_str_col_exists,
                                                   split_col_exists)

                performance_summary_dicts.append(general_performance_dict_for_group)
                all_bin_performances.extend(bin_performances)
                all_target_based_performances.append(target_based_score_perf)
            performance_summary_df = pd.DataFrame(performance_summary_dicts, columns=perf_sum_columns)
            detailed_performance_summary_df = pd.DataFrame(all_bin_performances,
                                                           columns=detailed_perf_sum_columns)
            target_based_summary_df = pd.DataFrame(all_target_based_performances,
                                                   columns=target_based_summary_columns)
        else:
            general_performance, bin_performances, target_based_score_perf = cls.__get_details(settings, settings.data)
            performance_summary_df = pd.DataFrame([general_performance], columns=perf_sum_columns)
            detailed_performance_summary_df = pd.DataFrame(bin_performances, columns=detailed_perf_sum_columns)
            target_based_summary_df = pd.DataFrame([target_based_score_perf],
                                                   columns=target_based_summary_columns)

        report = BinaryReport()
        report.performance_summary = performance_summary_df.T
        report.detailed_performance_summary = detailed_performance_summary_df
        report.target_based_performance_summary = target_based_summary_df.T
        return report

    @classmethod
    def __get_details(cls, settings, all_data):
        total_row_count = len(all_data)
        if settings.num_bins > total_row_count:
            raise ValueError("num_bins cannot be higher than number of rows in a set")
        bins = get_bins(all_data[settings.score_column], settings.num_bins)

        bin_dicts = []
        total_neg_count = 0
        total_pos_count = 0
        score_col = settings.score_column

        for bin_num in range(settings.num_bins):
            data = all_data.loc[bins == bin_num]
            total_count, positive_count, negative_count = cls.__get_row_positive_negative_count(data,
                                                                                                settings.target_column)

            bin_dicts.append({
                "BIN": bin_num,
                "TOTAL COUNT": total_count,
                "POSITIVE COUNT": positive_count,
                "NEGATIVE COUNT": negative_count,
                "TARGET RATIO": positive_count / total_count,
                "SCORE AVG": data[score_col].mean(),
                "SCORE SUM": data[score_col].sum(),
                "SCORE MIN": data[score_col].min(),
                "SCORE MAX": data[score_col].max(),
                "TRUE NEGATIVE COUNT": total_neg_count,
                "FALSE NEGATIVE COUNT": total_pos_count,
            })
            total_pos_count += positive_count
            total_neg_count += negative_count

        true_positive_count = 0
        false_positive_count = 0

        general_performance_dict = cls._get_general_performance_dict(all_data, settings, total_row_count,
                                                                     total_pos_count, total_neg_count)
        total_pos_ratio = general_performance_dict["POSITIVE RATIO"]
        pos_count_sum = 0
        total_count_sum = 0
        for bin_num in range(settings.num_bins - 1, -1, -1):
            bin_dict = bin_dicts[bin_num]
            true_positive_count += bin_dict["POSITIVE COUNT"]
            false_positive_count += bin_dict["NEGATIVE COUNT"]
            bin_dict["TRUE POSITIVE COUNT"] = true_positive_count
            bin_dict["FALSE POSITIVE COUNT"] = false_positive_count
            bin_dict["TRUE POSITIVE RATE"] = bin_dict["TRUE POSITIVE COUNT"] / (
                    bin_dict["TRUE POSITIVE COUNT"] + bin_dict["FALSE NEGATIVE COUNT"])
            bin_dict["FALSE POSITIVE RATE"] = bin_dict["FALSE POSITIVE COUNT"] / (
                    bin_dict["FALSE POSITIVE COUNT"] + bin_dict["TRUE NEGATIVE COUNT"])
            bin_dict["PRECISION"] = bin_dict["TRUE POSITIVE COUNT"] / (
                    bin_dict["TRUE POSITIVE COUNT"] + bin_dict["FALSE POSITIVE COUNT"])
            bin_dict["ACCURACY"] = (bin_dict["TRUE POSITIVE COUNT"] + bin_dict["TRUE NEGATIVE COUNT"]) / \
                                   ((bin_dict["TRUE POSITIVE COUNT"] + bin_dict["TRUE NEGATIVE COUNT"]) +
                                    (bin_dict["FALSE POSITIVE COUNT"] + bin_dict["FALSE NEGATIVE COUNT"]))
            bin_dict["F1 SCORE"] = cls.__get_f1_score(bin_dict["PRECISION"], bin_dict["TRUE POSITIVE RATE"])
            pos_count_sum += bin_dict["POSITIVE COUNT"]
            total_count_sum += bin_dict["TOTAL COUNT"]
            bin_dict["CUMULATIVE LIFT"] = pos_count_sum / total_count_sum / total_pos_ratio
        target_based_score_perf = cls._get_target_based_score_performance(settings, all_data, general_performance_dict)
        return general_performance_dict, bin_dicts, target_based_score_perf

    @classmethod
    def __get_f1_score(cls, precision, recall):
        if precision + recall != 0:
            return 2 * precision * recall / (precision + recall)
        return 0

    @classmethod
    def _get_target_based_score_performance(cls, settings, all_data: pd.DataFrame, general_performance_dict: dict):
        pos_count = general_performance_dict["POSITIVE COUNT"]
        neg_count = general_performance_dict["NEGATIVE COUNT"]
        pos_dict = cls._get_target_based_score_performance_for_target(settings, all_data, 1, "POSITIVES", pos_count)
        neg_dict = cls._get_target_based_score_performance_for_target(settings, all_data, 0, "NEGATIVES", neg_count)
        pos_dict.update(neg_dict)
        return pos_dict

    @classmethod
    def _get_target_based_score_performance_for_target(cls, settings, all_data: pd.DataFrame, target_val: int,
                                                       target_key_str: str,
                                                       count: int):
        score_col = settings.score_column
        pos_indices = all_data[settings.target_column] == target_val
        pos_data: pd.DataFrame = all_data[score_col].loc[pos_indices]

        percentile_nums = [0.05 * i for i in range(1, 20)]
        pos_percentiles = pos_data.quantile(percentile_nums)
        perf_dict = {
            f"{target_key_str} COUNT": count,
            f"{target_key_str} STD": pos_data.std(),
            f"{target_key_str} MEAN": pos_data.mean(),
            f"{target_key_str} MIN": pos_data.min(),
            f"{target_key_str} MAX": pos_data.max(),
        }

        for perc_num in percentile_nums:
            perf_dict[f"{target_key_str} P{int(perc_num * 100)}"] = pos_percentiles.loc[perc_num]
        return perf_dict

    @classmethod
    def _get_general_performance_dict(cls, all_data, settings,
                                      total_row_count: int, total_pos_count: int, total_neg_count: int):
        score_col = settings.score_column
        aggregates = all_data[score_col].agg(["mean", "std", "min", "max", "median"])
        percentiles = np.percentile(all_data[score_col], [25, 50, 75])
        general_performance_dict = {
            "ROW COUNT": total_row_count,
            "POSITIVE COUNT": total_pos_count,
            "NEGATIVE COUNT": total_neg_count,
            "POSITIVE RATIO": total_pos_count / total_row_count,
            "NEGATIVE RATIO": total_neg_count / total_row_count,
            "ODDS": total_pos_count / total_neg_count,
            "AUC": roc_auc_score(all_data[settings.target_column], all_data[score_col]),
            "SCORE AVG": aggregates["mean"],
            "SCORE STD": aggregates["std"],
            "SCORE MIN": aggregates["min"],
            "SCORE MAX": aggregates["max"],
            "SCORE P25": percentiles[0],
            "SCORE MEDIAN": percentiles[1],
            "SCORE P75": percentiles[2],
        }
        return general_performance_dict

    @classmethod
    def __add_group_values_to_dict(cls, dict_to_add: dict, group_tuple, id_str_col_exists: bool,
                                   split_col_exists: bool):
        if id_str_col_exists:
            dict_to_add["ID_STR"] = group_tuple[0]
            if split_col_exists:
                dict_to_add["SPLIT"] = group_tuple[1]
        elif split_col_exists:
            dict_to_add["SPLIT"] = group_tuple[0]

    @classmethod
    def __get_columns_for_performance_summary_df(cls, id_str_col_exists: bool, split_col_exists: bool):
        columns = ["AUC", "ROW COUNT", "POSITIVE COUNT", "NEGATIVE COUNT", "POSITIVE RATIO",
                   "NEGATIVE RATIO", "ODDS", "SCORE AVG", "SCORE STD", "SCORE MIN", "SCORE P25",
                   "SCORE MEDIAN", "SCORE P75", "SCORE MAX"]
        if split_col_exists:
            columns = ["SPLIT"] + columns
        if id_str_col_exists:
            columns = ["ID_STR"] + columns
        return columns

    @classmethod
    def __get_columns_for_detailed_performance_summary_df(cls, id_str_col_exists: bool, split_col_exists: bool):
        columns = ["BIN", "POSITIVE COUNT", "NEGATIVE COUNT", "TOTAL COUNT",
                   "TARGET RATIO", "SCORE AVG", "TRUE POSITIVE COUNT", "FALSE POSITIVE COUNT", "TRUE NEGATIVE COUNT",
                   "FALSE NEGATIVE COUNT", "TRUE POSITIVE RATE", "FALSE POSITIVE RATE", "PRECISION", "ACCURACY",
                   "F1 SCORE", "CUMULATIVE LIFT"]
        if split_col_exists:
            columns = ["SPLIT"] + columns
        if id_str_col_exists:
            columns = ["ID_STR"] + columns
        return columns

    @classmethod
    def __get_columns_for_target_based_performance_summary_df(cls, id_str_col_exists: bool, split_col_exists: bool):
        suffixes = ["COUNT", "STD", "MEAN", "MIN"]
        suffixes.extend([f"P{5 * i}" for i in range(1, 20)])
        suffixes.append("MAX")
        columns = [f"{prefix} {suffix}" for prefix in ["POSITIVES", "NEGATIVES"] for suffix in suffixes]
        if split_col_exists:
            columns = ["SPLIT"] + columns
        if id_str_col_exists:
            columns = ["ID_STR"] + columns
        return columns

    @classmethod
    def __get_row_positive_negative_count(cls, data: pd.DataFrame, target_col: str) -> Tuple[int, int, int]:
        row_count = cls._get_row_count(data)
        positive_count = np.sum(data[target_col] == 1)
        negative_count = row_count - positive_count
        return row_count, positive_count, negative_count
