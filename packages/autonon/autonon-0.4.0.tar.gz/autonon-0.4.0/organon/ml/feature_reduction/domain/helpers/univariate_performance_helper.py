"""Includes helper functions for univariate performance calculations"""
from itertools import chain
from typing import List, Dict, Tuple, Optional

import pandas as pd
from sklearn.model_selection import cross_val_score

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.common.enums.target_type import TargetType


def get_reduced_columns_via_performance(data: pd.DataFrame, target_column_name: str, target_type: TargetType,
                                        performance_metric, column_groups: List[List[str]],
                                        univariate_performance_results: Dict[str, float] = None,
                                        random_state=None) -> Tuple[List[str], Optional[Dict[str, float]]]:
    """
      Finds the reduced column using the univariate performance result.

      :return: Returns columns list which reduced and calculated performances for columns
        which are not in initial univariate_performances
      """
    existing_performances = {} if univariate_performance_results is None else univariate_performance_results
    all_cols = set(chain.from_iterable(column_groups))
    cols_to_calculate_performance = [col for col in all_cols if col not in existing_performances]
    reduced_columns = set()
    all_scores = existing_performances
    new_scores = None
    if len(cols_to_calculate_performance) > 0:
        new_scores = get_univariate_performances_for_columns(
            data, cols_to_calculate_performance,
            target_column_name, target_type, performance_metric,
            random_state
        )
        all_scores = {**existing_performances, **new_scores}
    for column_list in column_groups:
        score_results = {col: all_scores[col] for col in column_list if all_scores[col] is not None}
        if len(score_results) > 0:
            best_score_column = max(score_results, key=score_results.get)
            reduced_columns.update([col for col in score_results if col != best_score_column])
    return list(reduced_columns), new_scores


def get_univariate_performances_for_columns(data: pd.DataFrame, columns: List[str],
                                            target_column_name: str, target_type: TargetType,
                                            cross_val_scoring,
                                            random_state: int = None) -> Dict[str, float]:
    """Calculates univariate performances for given column. If column native type is not numeric or string,
    returned scores will be None
    """
    numeric_columns = [col for col in columns if
                       (get_column_native_type(data, col) == ColumnNativeType.Numeric)
                       ]
    string_columns = [col for col in columns if
                      (get_column_native_type(data, col) == ColumnNativeType.String)]
    model = _get_model(target_type, random_state)
    score_results = {}

    for column in columns:
        if column in numeric_columns:
            score = cross_val_score(model, data[[column]], data[target_column_name], cv=3,
                                    scoring=cross_val_scoring).mean()
        elif column in string_columns:
            score = cross_val_score(model, data[[column]].astype('category'),
                                    data[target_column_name], cv=3,
                                    scoring=cross_val_scoring).mean()
        else:
            score = None
        score_results[column] = score
    return score_results


def _get_model(target_type: TargetType, random_state: int):
    """
    Return Model with using target type.
    Parameters
    ----------
    target_type
    random_state

    Returns
    -------
    Returns Model object for LGBM
    """

    if target_type in (TargetType.BINARY, TargetType.MULTICLASS):
        from lightgbm import LGBMClassifier  # pylint: disable=import-outside-toplevel
        model = LGBMClassifier(random_state=random_state)
    else:
        from lightgbm import LGBMRegressor  # pylint: disable=import-outside-toplevel
        model = LGBMRegressor(random_state=random_state)
    return model
