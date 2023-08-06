"""Includes LightGBMRegressor class."""
from lightgbm import LGBMRegressor

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class LightGBMRegressor(BaseSklearnRegressor[LGBMRegressor]):
    """Wrapper for LGBMRegressor"""

    @property
    def regressor_class(self):
        return LGBMRegressor
