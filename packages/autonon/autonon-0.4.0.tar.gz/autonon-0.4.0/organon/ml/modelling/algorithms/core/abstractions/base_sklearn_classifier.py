"""Includes BaseSklearnClassifier class."""
import abc
from typing import TypeVar, Generic, Type, List, Dict, Any, Union

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_classifier import BaseClassifier

SklearnClassifierType = TypeVar("SklearnClassifierType")


class BaseSklearnClassifier(Generic[SklearnClassifierType], BaseClassifier, metaclass=abc.ABCMeta):
    """Base class for sklearn classifiers"""

    def __initialize_with_params(self, **params):
        # pylint: disable=attribute-defined-outside-init
        self._modeller: SklearnClassifierType = self.classifier_class(**params)

    @property
    @abc.abstractmethod
    def classifier_class(self) -> Type[SklearnClassifierType]:
        """Returns wrapped sklearn classifier class"""

    def _fit(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series], **kwargs):
        if isinstance(target_data, pd.DataFrame):
            target_data = target_data[target_data.columns[0]]
        self._modeller.fit(train_data, target_data, **kwargs)

    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame(self._modeller.predict(data))

    def _predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        """Predict score as probability"""
        return self._modeller.predict_proba(data)

    def _get_classes(self) -> List[str]:
        return self._modeller.classes_

    def _score(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series],
               sample_weight=None) -> float:
        return self._modeller.score(train_data, target_data)

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        return self.classifier_class().get_params()

    def get_params(self, deep=True):
        return self._modeller.get_params(deep=deep)

    def set_params(self, **params):
        self.__initialize_with_params(**params)
        return self
