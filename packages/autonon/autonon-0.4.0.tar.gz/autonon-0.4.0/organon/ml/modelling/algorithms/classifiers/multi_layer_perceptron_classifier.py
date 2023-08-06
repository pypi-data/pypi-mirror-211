"""Includes MultiLayerPerceptronClassifier class."""
from sklearn.neural_network import MLPClassifier

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class MultiLayerPerceptronClassifier(BaseSklearnClassifier[MLPClassifier]):
    """Wrapper for sklearn MLPClassifier"""

    @property
    def classifier_class(self):
        return MLPClassifier
