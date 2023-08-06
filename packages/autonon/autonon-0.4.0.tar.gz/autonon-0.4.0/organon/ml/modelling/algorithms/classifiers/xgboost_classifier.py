"""Includes XGBoostClassifier class."""
from xgboost import XGBClassifier

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_classifier import BaseSklearnClassifier


class XGBoostClassifier(BaseSklearnClassifier[XGBClassifier]):
    """Wrapper for XGBClassifier"""

    @property
    def classifier_class(self):
        return XGBClassifier
