"""Includes BaseClassifier class."""
import abc
from typing import List, Union

import pandas as pd
from sklearn.metrics import accuracy_score

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType


class BaseClassifier(BaseModeller, metaclass=abc.ABCMeta):
    """Base class for classifiers"""
    _estimator_type = "classifier"  # REQUIRED FOR SKLEARN GridSearch

    def predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        """Predict score as probability"""
        self._check_is_fitted()
        return self._predict_proba(data)

    @abc.abstractmethod
    def _predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @property
    def classes_(self):
        """Returns target class values in the same order as in return value of predict_proba"""
        # This property should return a valid value only after fit is called
        if not self.is_fitted():
            raise AttributeError("Modeller not fitted yet")
        return self._get_classes()

    @abc.abstractmethod
    def _get_classes(self) -> List[str]:
        """Returns target class values in the same order as in return value of predict_proba"""

    def _score(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series],
               sample_weight=None) -> float:
        return self.get_score_from_predictions(self.predict(train_data), target_data)

    @classmethod
    def get_score_from_predictions(cls, predictions: pd.DataFrame, actual: pd.DataFrame, sample_weight=None):
        """Calculates score from predictions and actual data"""
        return accuracy_score(actual, predictions, sample_weight=sample_weight)

    @property
    def modeller_type(self) -> ModellerType:
        return ModellerType.CLASSIFIER
