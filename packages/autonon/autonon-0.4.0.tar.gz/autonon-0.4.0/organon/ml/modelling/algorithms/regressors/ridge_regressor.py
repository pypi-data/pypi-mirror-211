"""Includes RidgeModeller class"""
from sklearn.linear_model import Ridge

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class RidgeRegressor(BaseSklearnRegressor[Ridge]):
    """Wrapper for sklearn ridge modeller"""

    @property
    def regressor_class(self):
        return Ridge
