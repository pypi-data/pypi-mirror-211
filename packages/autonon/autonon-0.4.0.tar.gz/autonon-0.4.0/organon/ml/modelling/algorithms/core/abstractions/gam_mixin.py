"""Includes GamMixin class."""
from typing import List, Dict, Any

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from statsmodels.stats.outliers_influence import variance_inflation_factor

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.ml.common.enums.target_type import TargetType
from organon.ml.preprocessing.services.preprocessor import Preprocessor


class GamMixin:
    """Mixin class including common gam functions"""

    def _fit_gam(self, train_data: pd.DataFrame, target_data: pd.Series):
        self._coarse_class = Preprocessor.get_coarse_class_service(0.2, target_column_type=self._get_target_type().name)
        self._coarse_class.fit(train_data, target_data)
        train_data = self._get_preprocessed(train_data)
        target_data = target_data.to_numpy(copy=False)
        self._initial_selected_features, self._best_alpha = self._get_initial_keep_list_and_best_alpha(train_data,
                                                                                                       target_data)
        keep_list = self._reduce_features(train_data, target_data)
        if len(keep_list) == 0:
            keep_list = train_data.columns.to_list()
        self._selected_features = keep_list
        self._model = self._fit_and_get_final_model(train_data, target_data, keep_list)
        return self._model

    def _get_preprocessed(self, data: pd.DataFrame):
        rejected_cols = self._coarse_class.fit_output.rejected_list
        if len(rejected_cols) > 0:
            data = data.drop(columns=[col for col in data.columns if col in rejected_cols])
        return self._coarse_class.transform(data)

    def _get_target_type(self) -> TargetType:
        raise NotImplementedError

    @property
    def final_model(self):
        """Returns final model"""
        return self._model

    @property
    def best_alpha(self):
        """Returns alpha value selected after GridSearchCV with Lasso"""
        return self._best_alpha

    @property
    def selected_features(self):
        """Returns column names selected after fit"""
        return self._selected_features

    @property
    def initial_selected_features(self):
        """Returns column names selected after GridSearchCV with Lasso"""
        return self._initial_selected_features

    def _fit_and_get_final_model(self, train_data: pd.DataFrame, target_data: np.ndarray, keep_list: List[str]):
        raise NotImplementedError

    def _get_initial_keep_list_and_best_alpha(self, train_data: pd.DataFrame, target_data: np.ndarray):
        param_grid = [{'alpha': self.grid_search_param_set, 'positive': [True]}]
        model = Lasso()
        grid_search = GridSearchCV(model, param_grid, cv=self.grid_search_cv, scoring=self.grid_search_scoring)
        grid_search.fit(train_data, target_data)

        lasso_coef_df_tmp = pd.DataFrame(grid_search.best_estimator_.coef_, columns=['coef'],
                                         index=train_data.columns).reset_index()
        keep_list = list(lasso_coef_df_tmp[lasso_coef_df_tmp['coef'] != 0]['index'].values)
        return keep_list, grid_search.best_params_['alpha']

    def _reduce_features(self, train_data: pd.DataFrame, target_data: np.ndarray) -> List[str]:
        raise NotImplementedError

    @classmethod
    def _get_feature_importances(cls, train_data: pd.DataFrame, target_data: np.ndarray):
        raise NotImplementedError

    @classmethod
    def _get_feature_to_remove(cls, train_data: pd.DataFrame, target_data: np.ndarray, keep_list: List[str],
                               candidate_features: List[str]):
        if len(candidate_features) == 1:
            return candidate_features[0]
        imp_df = cls._get_feature_importances(cls._get_cols(train_data, keep_list), target_data)
        imp_df.reset_index(inplace=True)
        imp_df.columns = ['feature', 'importance']
        imp_df = imp_df[imp_df["feature"].isin(candidate_features)].sort_values(by='importance')
        largest_vif_feature = imp_df.head(1)['feature'].values[0]
        return largest_vif_feature

    @classmethod
    def _get_keep_list(cls, train_data: pd.DataFrame, target_data: np.ndarray, keep_list_all: List[str],
                       best_alpha: float):
        if best_alpha == 0:
            model = Lasso(alpha=best_alpha, positive=True, max_iter=10000)
        else:
            model = Lasso(alpha=best_alpha, positive=True)
        data = cls._get_cols(train_data, keep_list_all)
        columns = data.columns.tolist()
        model.fit(data, target_data)
        del data
        lasso_coef_df_tmp = pd.DataFrame(model.coef_, columns=['coef'], index=columns).reset_index()
        keep_list = list(lasso_coef_df_tmp[lasso_coef_df_tmp['coef'] != 0]['index'].values)
        if len(keep_list) == 0:
            raise KnownException("No significant features found. Cannot build model.")
        return keep_list

    @classmethod
    def _get_vif_data(cls, train_data: pd.DataFrame, keep_list: List[str]):
        vif_data = pd.DataFrame()
        vif_data["feature"] = keep_list
        if len(keep_list) > 1:
            keep_df_arr = cls._get_cols(train_data, keep_list)
            vif_data["VIF"] = [variance_inflation_factor(keep_df_arr, i) for i in range(len(keep_list))]
        else:
            vif_data["VIF"] = [0]
        return vif_data

    @classmethod
    def _get_cols(cls, frame: pd.DataFrame, cols: List[str]):
        if sorted(frame.columns.tolist()) == sorted(cols):
            return frame  # prevents new copy of frame if all columns are wanted
        return frame[cols]

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        # pylint: disable=no-self-use
        return {
            "grid_search_param_set": np.arange(0, 2, 0.05).tolist(),
            "grid_search_cv": 10,
            "grid_search_scoring": "neg_mean_squared_error",
            "max_vif_limit": 5
        }
