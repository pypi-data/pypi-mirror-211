"""Includes VotingEnsembleRegressor class."""
from typing import Dict, Any, List, Union

import numpy as np
import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_regressor import BaseRegressor
from organon.ml.modelling.algorithms.helpers.ensembling_helper import get_voting_regressor_prediction


class VotingEnsembleRegressor(BaseRegressor):
    """VotingEnsembleRegressor"""

    # pylint: disable=no-member
    def _fit(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series], **kwargs):
        estimators: List[BaseRegressor] = self.estimators
        if estimators is None or len(estimators) == 0:
            raise ValueError("Estimators not given")
        for estimator in estimators:
            if not isinstance(estimator, BaseRegressor):
                raise ValueError("All estimators should be an instance of BaseRegressor")
        if not self.prefit:
            for estimator in estimators:
                estimator.fit(train_data, target_data)

    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        estimators: List[BaseRegressor] = self.estimators
        prediction_dfs = [estimator.predict(data) for estimator in estimators]
        predictions = np.asarray([pred.iloc[:, 0] for pred in prediction_dfs]).T
        final_pred = get_voting_regressor_prediction(predictions)
        return pd.DataFrame({prediction_dfs[0].columns[0]: final_pred})

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        return {
            "estimators": None,
            "prefit": False,
        }
