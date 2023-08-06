"""Includes RFClassifier class."""
from sklearn.ensemble import RandomForestClassifier

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class RFClassifier(BaseSklearnClassifier[RandomForestClassifier]):
    """Wrapper for sklearn RandomForestClassifier"""

    @property
    def classifier_class(self):
        return RandomForestClassifier
