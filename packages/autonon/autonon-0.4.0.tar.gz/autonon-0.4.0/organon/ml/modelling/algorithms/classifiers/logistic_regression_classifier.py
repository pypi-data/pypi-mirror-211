"""Includes LogisticRegressionClassifier class."""
from sklearn.linear_model import LogisticRegression

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class LogisticRegressionClassifier(BaseSklearnClassifier[LogisticRegression]):
    """Wrapper for sklearn LogisticRegression"""

    @property
    def classifier_class(self):
        return LogisticRegression
