""" todo docstring """
import math
from typing import List

import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor

from organon.idq.domain.controls.helpers.algorithms.base_predictor import BasePredictor
from organon.idq.domain.controls.helpers.algorithms.prediction_result import PredictionResult


class RandomForestPredictor(BasePredictor):
    """ todo docstring """

    @staticmethod
    def predict(input_data: List[float], t_val: float, n_estimators=200, max_depth=10,
                max_samples_leaf=1) -> PredictionResult:
        """randomforestregressor prediction, input_data from t-n to t-1"""
        rf_ = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, min_samples_leaf=max_samples_leaf)
        features, labels = RandomForestPredictor.generate_train_data_with_lags(input_data, t_val)
        impute_value = float(np.finfo(np.float32).min)
        normalized_features = np.nan_to_num(features, nan=impute_value)
        features_to_fit = features[:-1]
        labels_to_fit = labels[:-1]
        nan_indices = [i for i, val in enumerate(labels_to_fit) if math.isnan(val)]
        features_nan_target_removed = np.nan_to_num(np.delete(features_to_fit, nan_indices, axis=0), nan=impute_value)
        labels_nan_removed = [val for val in labels_to_fit if not math.isnan(val)]
        rf_.fit(features_nan_target_removed, labels_nan_removed)

        predictions = rf_.predict(normalized_features)
        pred_result = PredictionResult(labels)
        pred_result.predictions = predictions
        past_values_predictions = np.delete(predictions[:-1], nan_indices, axis=0)
        pred_result.mean_square_err = metrics.mean_squared_error(labels_nan_removed, past_values_predictions)
        return pred_result
