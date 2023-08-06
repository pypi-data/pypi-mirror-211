""" This module includes ComparisonHelperFunctions"""
import math
from typing import Tuple

from organon.idq.domain.enums.signal_type import SignalType


class ComparisonHelperFunctions:
    """ Class for ComparisonHelperFuncstions """

    @staticmethod
    def get_traffic_light_signal(change: float, yellow_threshold: float, green_threshold: float) -> SignalType:
        """ :returns signal type"""
        if change is None:
            return SignalType.GREEN
        if change < green_threshold:
            return SignalType.GREEN
        if change < yellow_threshold:
            return SignalType.YELLOW
        return SignalType.RED

    @staticmethod
    def get_percentage_change(current: float, reference: float) -> float:
        """:returns percentage change of current value"""
        delta = reference - current
        if current == 0 and reference == 0:
            return 0
        if reference == 0:
            return 1
        return abs(delta / reference)

    @staticmethod
    def compute_control_mean_std_avg(data: list) -> Tuple[float, float]:
        """computes mean and std for past data"""
        weight = 0.0
        variance = 0.0
        mean = 0.0
        val_sum = 0.0
        for val in data:
            delta = val - mean
            weight += 1.0
            variance += delta * delta * (1.0 - (1.0 * 1.0) / weight)
            mean += delta * (1.0 / weight)
            val_sum += val
        if weight >= 2.0:
            variance = variance / (weight - 1)
        std_error = math.sqrt(variance) / math.sqrt(len(data))
        return mean, std_error

    @staticmethod
    def is_outside_confidence_interval(z_score: float, control_mean: float, control_std_err: float,
                                       test_mean: float) -> bool:
        """ColumnMeanIsOutsideMeanConfidenceInterval control"""
        upper_limit = control_mean + z_score * control_std_err
        lower_limit = control_mean - z_score * control_std_err
        if test_mean < lower_limit or test_mean > upper_limit:
            return True
        return False
