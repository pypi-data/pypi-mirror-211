"""Includes GamClassifier class."""
from typing import List, Union, Dict, Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_native_type_from_dtype
from organon.fl.mathematics.constants import DOUBLE_MAX
from organon.ml.common.enums.target_type import TargetType
from organon.ml.modelling.algorithms.core.abstractions.base_classifier import BaseClassifier
from organon.ml.modelling.algorithms.core.abstractions.gam_mixin import GamMixin
from organon.ml.preprocessing.helpers import preprocessing_input_helper


class GamClassifier(GamMixin, BaseClassifier):
    """Generalized additive modelling classifier"""

    # pylint: disable=no-member
    def _fit(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series], **kwargs):
        if isinstance(target_data, pd.DataFrame):
            target_data = target_data[target_data.columns[0]]
        n_unique_classes = target_data.nunique()
        if n_unique_classes > 2:
            raise ValueError("GamClassifier cannot be used for multiclass targets")

        # pylint: disable=attribute-defined-outside-init
        self._target_not_numeric = get_native_type_from_dtype(target_data.dtype) != ColumnNativeType.Numeric
        if self._target_not_numeric:
            if self.target_positive_class is None or self.target_negative_class is None:
                raise ValueError("Target positive and negative classes should be given for non-numeric target data")
            target_data = preprocessing_input_helper.convert_str_series_to_binary(target_data,
                                                                                  self.target_positive_class,
                                                                                  self.target_negative_class)

        self._fit_gam(train_data, target_data)
        return self

    def _predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self._get_preprocessed(data)
        classes = list(self._model.classes_)
        if self._target_not_numeric:
            classes = preprocessing_input_helper.convert_binary_series_to_str(pd.Series(classes),
                                                                              self.target_positive_class,
                                                                              self.target_negative_class)
        return pd.DataFrame(self._model.predict_proba(data[self._selected_features]),
                            columns=classes)

    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self._get_preprocessed(data)
        prediction = pd.Series(self._model.predict(data[self._selected_features]))
        if self._target_not_numeric:
            prediction = preprocessing_input_helper.convert_binary_series_to_str(prediction, self.target_positive_class,
                                                                                 self.target_negative_class)
        return pd.DataFrame(prediction.values, columns=["prediction"])

    def _get_classes(self) -> List[str]:
        return list(self._model.classes_)

    def _get_target_type(self) -> TargetType:
        return TargetType.BINARY

    def _fit_and_get_final_model(self, train_data: pd.DataFrame, target_data: np.ndarray, keep_list: List[str]):
        regression_model = LogisticRegression()
        regression_model.fit(self._get_cols(train_data, keep_list), target_data)
        return regression_model

    def _reduce_features(self, train_data: pd.DataFrame, target_data: np.ndarray) -> List[str]:
        rejected_list = []
        negative_coef_exists = True
        max_vif = DOUBLE_MAX
        keep_list_all = train_data.columns.tolist()
        while max_vif > self.max_vif_limit or negative_coef_exists:
            keep_list = self._get_keep_list(train_data, target_data, keep_list_all, self._best_alpha)
            vif_data = self._get_vif_data(train_data, keep_list)
            coef_df = self._get_coef_df(train_data, target_data, keep_list)
            negative_coef_exists = sum(coef_df['coef'] < 0) > 0
            max_vif = vif_data["VIF"].max()

            if max_vif > self.max_vif_limit or negative_coef_exists:
                vif_data = pd.merge(vif_data, coef_df, how='left', on='feature')
                to_eliminate = \
                    vif_data[(vif_data['VIF'] > self.max_vif_limit) | (vif_data['coef'] < 0)]["feature"].tolist()

                rejected_list.append(self._get_feature_to_remove(train_data, target_data, keep_list, to_eliminate))
                keep_list_all = [x for x in keep_list_all if x not in rejected_list]
                if len(keep_list_all) == 0:
                    return []
        return keep_list

    @classmethod
    def _get_feature_importances(cls, train_data: pd.DataFrame, target_data: np.ndarray) -> pd.DataFrame:
        rf_classifier = RandomForestClassifier()
        rf_classifier.fit(train_data, target_data)
        return pd.DataFrame(rf_classifier.feature_importances_, columns=['importance'], index=train_data.columns)

    @classmethod
    def _get_coef_df(cls, train_data: pd.DataFrame, target_data: np.ndarray, keep_list: List[str]):
        regression_model = LogisticRegression()
        data = cls._get_cols(train_data, keep_list)
        columns = data.columns.tolist()
        regression_model.fit(data, target_data)
        del data
        coef_df = pd.DataFrame(regression_model.coef_, columns=columns).T
        coef_df = coef_df.reset_index()
        coef_df.columns = ['feature', 'coef']
        return coef_df

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        params = super()._get_params_with_defaults()
        params.update({
            "target_positive_class": None,
            "target_negative_class": None
        })
        return params
