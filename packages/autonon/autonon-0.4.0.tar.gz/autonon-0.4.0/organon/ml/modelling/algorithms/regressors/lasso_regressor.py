"""Includes LassoRegressor class"""
from sklearn.linear_model import Lasso

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class LassoRegressor(BaseSklearnRegressor[Lasso]):
    """Wrapper for sklearn lasso modeller"""

    @property
    def regressor_class(self):
        return Lasso
