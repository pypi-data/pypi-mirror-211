"""Includes StackingEnsembleClassifier class"""
from typing import Dict, Any

from sklearn.ensemble import StackingClassifier

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class StackingEnsembleClassifier(BaseSklearnClassifier):
    """Wrapper for sklearn StackingClassifier"""

    @property
    def classifier_class(self):
        return StackingClassifier

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        return StackingClassifier(estimators=[]).get_params()
