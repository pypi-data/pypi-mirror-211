"""Includes GBMRegressor class."""
from sklearn.ensemble import GradientBoostingRegressor

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class GBMRegressor(BaseSklearnRegressor[GradientBoostingRegressor]):
    """Wrapper for sklearn GradientBoostingRegressor"""

    @property
    def regressor_class(self):
        return GradientBoostingRegressor
