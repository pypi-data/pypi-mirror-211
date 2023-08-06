"""Includes GBMClassifier class."""
from sklearn.ensemble import GradientBoostingClassifier

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class GBMClassifier(BaseSklearnClassifier[GradientBoostingClassifier]):
    """Wrapper for sklearn GradientBoostingClassifier"""

    @property
    def classifier_class(self):
        return GradientBoostingClassifier
