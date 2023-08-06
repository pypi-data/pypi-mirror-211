"""Includes GamRegressor class."""
from typing import Union, List

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from organon.fl.mathematics.constants import DOUBLE_MAX
from organon.ml.common.enums.target_type import TargetType
from organon.ml.modelling.algorithms.core.abstractions.base_regressor import BaseRegressor
from organon.ml.modelling.algorithms.core.abstractions.gam_mixin import GamMixin


class GamRegressor(GamMixin, BaseRegressor):
    """Generalized additive modelling regressor"""

    # pylint:disable=no-member

    def _fit(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series], **kwargs):
        if isinstance(target_data, pd.DataFrame):
            target_data = target_data[target_data.columns[0]]
        return self._fit_gam(train_data, target_data)

    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self._get_preprocessed(data)
        return pd.DataFrame(self._model.predict(data[self._selected_features]), columns=["prediction"])

    def _get_target_type(self) -> TargetType:
        return TargetType.SCALAR

    def _fit_and_get_final_model(self, train_data: pd.DataFrame, target_data: np.ndarray, keep_list: List[str]):
        regression_model = LinearRegression(positive=True)
        regression_model.fit(self._get_cols(train_data, keep_list), target_data)
        return regression_model

    def _reduce_features(self, train_data: pd.DataFrame, target_data: np.ndarray) -> List[str]:
        rejected_list = []
        max_vif = DOUBLE_MAX
        keep_list_all = train_data.columns.tolist()
        while max_vif > self.max_vif_limit:
            keep_list = self._get_keep_list(train_data, target_data, keep_list_all, self._best_alpha)
            vif_data = self._get_vif_data(train_data, keep_list)
            max_vif = vif_data["VIF"].max()
            if max_vif > self.max_vif_limit:
                to_eliminate = vif_data[(vif_data['VIF'] > self.max_vif_limit)]["feature"].tolist()
                rejected_list.append(self._get_feature_to_remove(train_data, target_data, keep_list, to_eliminate))
                keep_list_all = [x for x in keep_list_all if x not in rejected_list]
        return keep_list

    @classmethod
    def _get_feature_importances(cls, train_data: pd.DataFrame, target_data: np.ndarray) -> pd.DataFrame:
        rf_regressor = RandomForestRegressor()
        rf_regressor.fit(train_data, target_data)
        return pd.DataFrame(rf_regressor.feature_importances_, columns=['importance'], index=train_data.columns)
