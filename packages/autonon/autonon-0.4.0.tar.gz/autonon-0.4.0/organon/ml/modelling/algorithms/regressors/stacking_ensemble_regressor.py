"""Includes StackingEnsembleRegressor class"""
from typing import Dict, Any

from sklearn.ensemble import StackingRegressor

from organon.ml.modelling.algorithms.core.abstractions.base_sklearn_regressor import BaseSklearnRegressor


class StackingEnsembleRegressor(BaseSklearnRegressor):
    """Wrapper for sklearn StackingRegressor"""

    @property
    def regressor_class(self):
        return StackingRegressor

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        return StackingRegressor(estimators=[]).get_params()
