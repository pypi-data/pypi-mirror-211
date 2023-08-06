"""Includes Modeller enum class."""
from enum import Enum, auto

from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType


class Modeller(Enum):
    """Modellers"""
    LOGISTIC_REGRESSION_CLASSIFIER = auto()
    GAM_CLASSIFIER = auto()
    RF_CLASSIFIER = auto()
    GBM_CLASSIFIER = auto()
    LIGHTGBM_CLASSIFIER = auto()
    XGBOOST_CLASSIFIER = auto()
    MULTI_LAYER_PERCEPTRON_CLASSIFIER = auto()
    RIDGE = auto()
    GAM_REGRESSOR = auto()
    LASSO = auto()
    RANDOM_FOREST_REGRESSOR = auto()
    GBM_REGRESSOR = auto()
    LIGHTGBM_REGRESSOR = auto()
    XGBOOST_REGRESSOR = auto()
    MULTI_LAYER_PERCEPTRON_REGRESSOR = auto()

    def get_modeller_type(self):
        """Returns type of modeller"""
        if self in [Modeller.LOGISTIC_REGRESSION_CLASSIFIER, Modeller.GAM_CLASSIFIER, Modeller.RF_CLASSIFIER,
                    Modeller.GBM_CLASSIFIER, Modeller.LIGHTGBM_CLASSIFIER, Modeller.XGBOOST_CLASSIFIER,
                    Modeller.MULTI_LAYER_PERCEPTRON_CLASSIFIER]:
            return ModellerType.CLASSIFIER
        return ModellerType.REGRESSOR
