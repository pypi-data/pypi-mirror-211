""" This module includes BasePredictor class"""
import abc
from collections import deque
from typing import Tuple, List

import numpy as np

from organon.idq.domain.controls.helpers.algorithms.prediction_result import PredictionResult
from organon.idq.domain.enums.dq_pred_algorithm_type import DqPredAlgorithmType


class BasePredictor(metaclass=abc.ABCMeta):
    """ Base class for prediction"""

    def __init__(self):
        self.predictor_type: DqPredAlgorithmType = None

    @staticmethod
    @abc.abstractmethod
    def predict(input_data: list, t_val: float, n_estimators=200, max_depth=10,
                max_samples_leaf=1) -> PredictionResult:
        """ train and predict data """
        raise NotImplementedError

    @staticmethod
    def generate_train_data_with_lags(past_data: List[float], t_val: float) -> \
            Tuple[np.array, List[float]]:
        """model data generator"""
        input_data = past_data.copy()
        benchmark_horizon = len(input_data)
        input_data.append(t_val)
        labels = input_data
        items = deque(input_data)
        trend_list = deque(range(1, len(input_data) + 1))
        if benchmark_horizon < 5:
            return np.array([trend_list]).T, labels
        if benchmark_horizon < 12:
            lag_num = 1
        elif benchmark_horizon < 24:
            lag_num = 3
        elif benchmark_horizon < 48:
            lag_num = 7
        else:
            lag_num = 14
        lag_list = []
        for _ in range(lag_num):
            items.rotate(1)
            lag_list.append(list(items))
            trend_list.rotate(1)
        return np.append(np.array([list(trend_list)]), np.array(lag_list), 0)[:, lag_num:].T, labels[lag_num:]
