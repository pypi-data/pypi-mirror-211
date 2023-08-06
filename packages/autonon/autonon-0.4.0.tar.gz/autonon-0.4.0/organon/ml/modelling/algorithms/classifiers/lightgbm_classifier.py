"""Includes LGBMClassifier class."""
from lightgbm import LGBMClassifier

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class LightGBMClassifier(BaseSklearnClassifier[LGBMClassifier]):
    """Wrapper for LGBMClassifier"""

    @property
    def classifier_class(self):
        return LGBMClassifier
