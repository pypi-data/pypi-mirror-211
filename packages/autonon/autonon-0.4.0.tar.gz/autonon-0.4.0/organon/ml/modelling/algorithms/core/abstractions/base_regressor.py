"""Includes BaseRegressor class."""
import abc
from typing import Union

import pandas as pd
from sklearn.metrics import r2_score

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType


class BaseRegressor(BaseModeller, metaclass=abc.ABCMeta):
    """Base class for regressors"""
    _estimator_type = "regressor"  # REQUIRED FOR SKLEARN GridSearch

    def _score(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series],
               sample_weight=None) -> float:
        y_pred = self.predict(train_data)
        return r2_score(target_data, y_pred, sample_weight=sample_weight)

    @property
    def modeller_type(self) -> ModellerType:
        return ModellerType.REGRESSOR
