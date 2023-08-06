"""Includes RFRegressor class."""
from sklearn.ensemble import RandomForestRegressor

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class RFRegressor(BaseSklearnRegressor[RandomForestRegressor]):
    """Wrapper for sklearn RandomForestRegressor"""

    @property
    def regressor_class(self):
        return RandomForestRegressor
