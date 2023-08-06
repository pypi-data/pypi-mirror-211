"""todo"""
import math
from typing import List, Dict

from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.core.collections.sorted_dict import SortedDict
from organon.fl.mathematics.helpers.dataframe_operations_factory import DataFrameOperationsFactory
from organon.fl.mathematics.helpers.idataframe_operations import IDataFrameOperations
from organon.idq.core.dq_constants import DqConstants
from organon.idq.domain.businessobjects.statistics.dq_categorical_statistics import DqCategoricalStatistics
from organon.idq.domain.businessobjects.statistics.dq_sample_numerical_statistics import DqSampleNumericalStatistics
from organon.idq.domain.helpers.statistics.dq_statistical_functions import DqStatisticalFunctions


class DqStatisticsDomainService:
    """todo"""

    @staticmethod
    def compute_categorical_statistics(data_frame: IDataFrame,
                                       missing_values_by_col: Dict[str, List[str]]) \
            -> Dict[str, DqCategoricalStatistics]:
        """Computes nominal statistics for all columns given in missing_values_by_col"""
        df_operations = DataFrameOperationsFactory.get_dataframe_operations(data_frame)

        stats_per_col = {}
        for col, missing_values in missing_values_by_col.items():
            missing_frequencies = df_operations.get_frequencies(data_frame, col, missing_values)
            n_val = df_operations.get_size(data_frame)
            frequencies = df_operations.get_frequencies(data_frame, col)
            stats = DqCategoricalStatistics(missing_values, frequencies)
            stats.n_val = n_val
            stats.n_miss = sum(missing_frequencies.values())
            stats.cardinality = len(frequencies)
            stats_per_col[col] = stats
        return stats_per_col

    @staticmethod
    def compute_numerical_statistics(data_frame: IDataFrame,
                                     missing_values_by_col: Dict[str, List[float]],
                                     tukey_parameter=1.5):
        """Computes numerical statistics for all columns given in missing_values_by_col"""
        df_operations = DataFrameOperationsFactory.get_dataframe_operations(data_frame)

        stats_per_col = {}
        for col, missing_values in missing_values_by_col.items():
            missing_frequencies = df_operations.get_frequencies(data_frame, col, missing_values)
            col_without_missing = df_operations.get_col_df_without_values(data_frame, col, missing_values)
            n_val = df_operations.get_size(col_without_missing)
            if n_val == 0:
                stats_per_col[col] = DqStatisticsDomainService.__get_null_stats(missing_frequencies)
                continue
            stats = DqStatisticsDomainService.__get_stats_for_column(df_operations, col_without_missing, col,
                                                                     missing_frequencies, n_val, tukey_parameter)
            stats_per_col[col] = stats
        return stats_per_col

    @staticmethod
    def __get_stats_for_column(df_operations: IDataFrameOperations, col_without_missing: IDataFrame, col: str,
                               missing_frequencies: Dict[float, int], n_val: int,
                               tukey_parameter: float):
        cardinality = df_operations.get_column_distinct_counts(col_without_missing, col_names=[col])[col]
        compute_freqs = cardinality <= DqConstants.NUMERICAL_STATISTICS_MIN_CARDINALITY

        freqs = {}
        if compute_freqs:
            freqs = df_operations.get_frequencies(col_without_missing, col)
        stats = DqSampleNumericalStatistics()
        stats.missing_values = list(missing_frequencies.keys())
        stats.n_val = n_val
        stats.n_miss = sum(missing_frequencies.values())
        stats.frequencies = SortedDict(freqs)
        stats.compute_frequencies = compute_freqs
        stats.missing_values_frequencies = missing_frequencies
        stats.cardinality = cardinality
        stats.mean = df_operations.get_mean_value(col_without_missing, col, skipna=False)
        stats.min = df_operations.get_min_value(col_without_missing, col, skipna=False)
        stats.max = df_operations.get_max_value(col_without_missing, col, skipna=False)
        stats.sum = df_operations.get_sum_value(col_without_missing, col, skipna=False)

        stats.variance = df_operations.get_variance_value(col_without_missing, col, skipna=False)
        stats.std_dev = math.sqrt(stats.variance)
        stats.percentile_values = SortedDict(df_operations.get_percentile_values(
            col_without_missing, col, DqConstants.DEFAULT_PERCENTILE_LIST))
        stats.quartile_values = SortedDict(df_operations.get_percentile_values(col_without_missing, col,
                                                                               [25, 50, 75]))

        stats.median = stats.quartile_values[50]
        DqStatisticsDomainService.__set_interval_stats_and_trimmed_mean(df_operations, stats, col_without_missing,
                                                                        col, tukey_parameter)
        return stats

    @staticmethod
    def __set_interval_stats_and_trimmed_mean(df_operations: IDataFrameOperations,
                                              stats: DqSampleNumericalStatistics,
                                              col_without_missing: IDataFrame, col: str,
                                              tukey_parameter: float):
        DqStatisticsDomainService.__set_quartile_statistics(stats, tukey_parameter)
        if stats.n_val != 1:
            modified_number_of_intervals = min(DqConstants.NUMERICAL_STATISTICS_MAX_NUM_OF_INTERVALS, stats.n_val)
            frequencies = stats.frequencies
            if frequencies is None or len(frequencies) == 0:
                frequencies = SortedDict(df_operations.get_frequencies(col_without_missing, col))
            stats.interval_statistics = DqStatisticalFunctions.get_balanced_intervals_and_statistics(
                frequencies, modified_number_of_intervals, DqConstants.NUMERICAL_STATISTICS_MIN_INTERVAL_SIZE)
            stats.trimmed_mean = df_operations.get_trimmed_mean_value(col_without_missing, col,
                                                                      stats.tukey_lower_limit,
                                                                      stats.tukey_upper_limit)
        else:
            stats.trimmed_mean = stats.mean

    @staticmethod
    def __get_null_stats(missing_values_frequencies):
        n_miss = sum(missing_values_frequencies.values())
        null_stats = DqSampleNumericalStatistics.get_null_statistics()
        null_stats.missing_values = list(missing_values_frequencies.keys())
        null_stats.frequencies = SortedDict()
        null_stats.missing_values_frequencies = SortedDict(missing_values_frequencies)
        null_stats.n_val = n_miss
        null_stats.n_miss = n_miss
        null_stats.cardinality = 0
        return null_stats

    @staticmethod
    def __set_quartile_statistics(stats: DqSampleNumericalStatistics, tukey_parameter: float):
        quartile_75 = stats.quartile_values[75]
        quartile_25 = stats.quartile_values[25]
        stats.inter_quartile_range = quartile_75 - quartile_25
        delta = tukey_parameter * stats.inter_quartile_range
        stats.tukey_lower_limit = quartile_25 - delta
        stats.tukey_upper_limit = quartile_75 + delta
