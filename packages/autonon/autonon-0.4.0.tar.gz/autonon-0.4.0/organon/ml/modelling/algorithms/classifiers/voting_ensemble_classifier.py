"""Includes VotingEnsembleClassifier class."""
from typing import Dict, Any, List, Union

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_classifier import BaseClassifier
from organon.ml.modelling.algorithms.helpers.ensembling_helper import get_voting_classifier_prediction


class VotingEnsembleClassifier(BaseClassifier):
    """VotingEnsembleClassifier"""

    # pylint: disable=no-member

    def _predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        estimators: List[BaseClassifier] = self.estimators
        columns = estimators[0].classes_
        prediction_dfs = (estimator.predict_proba(data).loc[:, columns] for estimator in estimators)  # generator
        average_probas = sum(prediction_dfs) / len(estimators)

        return average_probas

    def _fit(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series], **kwargs):
        estimators: List[BaseClassifier] = self.estimators
        if estimators is None or len(estimators) == 0:
            raise ValueError("Estimators not given")
        for estimator in estimators:
            if not isinstance(estimator, BaseClassifier):
                raise ValueError("All estimators should be an instance of BaseClassifier")
        if not self.prefit:
            for estimator in estimators:
                estimator.fit(train_data, target_data)

    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        estimators: List[BaseClassifier] = self.estimators
        all_pred_df = pd.DataFrame()
        target_col_name = None
        for i, estimator in enumerate(estimators):
            pred_df = estimator.predict(data)
            target_col_name = pred_df.columns.tolist()[0]
            all_pred_df[f"pred_{i}"] = pred_df.iloc[:, 0]
        final_pred = get_voting_classifier_prediction(all_pred_df)
        return pd.DataFrame({target_col_name: final_pred})

    def _get_params_with_defaults(self) -> Dict[str, Any]:
        return {
            "estimators": None,
            "prefit": False,
        }

    def _get_classes(self) -> List[str]:
        return self.estimators[0].classes_  # predict_proba should return df with this column order too
