"""Includes MultiLayerPerceptronRegressor class."""
from sklearn.neural_network import MLPRegressor

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class MultiLayerPerceptronRegressor(BaseSklearnRegressor[MLPRegressor]):
    """Wrapper for sklearn MLPRegressor"""

    @property
    def regressor_class(self):
        return MLPRegressor
