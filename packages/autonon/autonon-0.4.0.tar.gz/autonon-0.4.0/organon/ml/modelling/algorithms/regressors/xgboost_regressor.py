"""Includes XGBoostRegressor class."""
from xgboost import XGBRegressor

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class XGBoostRegressor(BaseSklearnRegressor[XGBRegressor]):
    """Wrapper for XGBRegressor"""

    @property
    def regressor_class(self):
        return XGBRegressor
