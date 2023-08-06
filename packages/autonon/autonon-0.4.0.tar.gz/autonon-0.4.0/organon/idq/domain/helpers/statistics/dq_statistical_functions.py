"""Includes DqStatisticalFunctions class."""
from typing import Dict, Tuple, TypeVar

import numpy as np

from organon.fl.core.collections.sorted_dict import SortedDict
from organon.fl.mathematics.businessobjects.sets.interval import Interval
from organon.fl.mathematics.businessobjects.sets.sum_triple import SumTriple
from organon.fl.mathematics.constants import DOUBLE_MIN, NEGATIVE_INFINITY, POSITIVE_INFINITY
from organon.fl.mathematics.enums.sets.interval_type import IntervalType

T = TypeVar("T")


class DqStatisticalFunctions:
    """Includes helper functions for dq statistics."""

    @staticmethod
    def get_percentages_from_frequencies_for_sorted(frequencies: SortedDict[object, float]) -> \
            SortedDict[object, float]:
        """todo"""
        total = sum(frequencies.values())
        return SortedDict({key: value / total for key, value in frequencies.items()})

    @staticmethod
    def get_percentages_from_frequencies(frequencies: Dict[object, float]) -> Dict[object, float]:
        """todo"""
        total = sum(frequencies.values())
        return {key: value / total for key, value in frequencies.items()}

    @staticmethod
    def get_balanced_intervals_and_statistics(frequencies: SortedDict[float, int],
                                              max_num_of_intervals: float,
                                              min_bucket_size: int) -> SortedDict[Interval, SumTriple]:
        """Get balanced intervals and statistics for interval_statistics of stats"""
        if frequencies is None:
            raise Exception("Frequencies is null as input to GetBalancedIntervals method")
        values_length = sum(frequencies.values())
        if values_length == 0:
            raise Exception("Frequencies is empty as input to GetBalancedIntervals method")
        if max_num_of_intervals <= 1:
            raise Exception(
                "Maximum-number-of-intervals argument must be greater than 1 as input to GetBalancedIntervals method")
        if values_length < max_num_of_intervals:
            raise Exception(
                "Maximum-number-of-intervals argument must be less than array length as"
                " input to GetBalancedIntervals method")
        window = int(float(values_length) / max_num_of_intervals)
        lower_bound = NEGATIVE_INFINITY
        cum = 0
        triple = SumTriple()
        interval_dict: SortedDict[Interval, SumTriple] = SortedDict()
        updated_bucket_size = int(max(window * 0.2, min_bucket_size))
        for order, (frequency_key, frequency_value) in enumerate(frequencies.items()):
            cum = cum + frequency_value
            triple.update_with_data(frequency_value, frequency_key)
            if order == (len(frequencies) - 1):
                if (len(interval_dict) > 0) & (cum < updated_bucket_size):
                    last_interval = interval_dict.keys()[len(interval_dict) - 1].deep_copy()
                    last_triple = interval_dict.values()[len(interval_dict) - 1]
                    modified_triple = SumTriple(last_triple.count, last_triple.sum_, last_triple.sum_of_squares)
                    modified_triple.update_with_sum_triple(triple)
                    interval_dict.popitem()
                    modified_interval = Interval("", last_interval.lower_bound, POSITIVE_INFINITY,
                                                 IntervalType.OPEN_CLOSED)
                    interval_dict[modified_interval] = modified_triple
                else:
                    interval = Interval("", lower_bound, POSITIVE_INFINITY, IntervalType.OPEN_CLOSED)
                    interval_dict[interval] = triple
            elif cum >= window:
                upper_bound = frequency_key
                interval = Interval("", lower_bound, upper_bound, IntervalType.OPEN_CLOSED)
                interval_dict[interval] = triple
                lower_bound = upper_bound
                cum = 0
                triple = SumTriple()
        return interval_dict

    @staticmethod
    def population_stability_index(left_frequency: Dict[T, float] or SortedDict[str, float],
                                   right_frequency: Dict[T, float] or SortedDict[str, float],
                                   minimum_injection: int) -> Tuple[T, float]:
        """Return population stability index value"""

        union_key = list(left_frequency.keys() | right_frequency.keys())
        updated_left_frequency = {}
        updated_right_frequency = {}
        for item in union_key:
            updated_left_frequency[item] = left_frequency[item] if (
                    item in left_frequency and left_frequency[item] > 0) else minimum_injection

            updated_right_frequency[item] = right_frequency[item] if (
                    item in right_frequency and right_frequency[item] > 0) else minimum_injection

        left_percentages = DqStatisticalFunctions.get_percentages_from_frequencies(updated_left_frequency)
        right_percentages = DqStatisticalFunctions.get_percentages_from_frequencies(updated_right_frequency)
        return DqStatisticalFunctions._get_population_stability_index(left_percentages, right_percentages)

    @staticmethod
    def _get_population_stability_index(left_percentages: Dict[T, float],
                                        right_percentages: Dict[T, float]) -> Tuple[T, float]:

        max_ = DOUBLE_MIN
        max_category = None
        sum_ = 0.0
        for item_key, item_value in left_percentages.items():
            left_percentage = item_value
            right_percentage = right_percentages[item_key]
            current = (left_percentage - right_percentage) * np.log(left_percentage / right_percentage)
            sum_ = sum_ + current
            if current >= max_:
                max_ = current
                max_category = item_key
        return max_category, sum_
