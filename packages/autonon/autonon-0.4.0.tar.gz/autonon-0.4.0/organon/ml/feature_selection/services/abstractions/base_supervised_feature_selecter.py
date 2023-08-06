"""Includes BaseSupervisedFeatureSelecter class"""
import abc
from typing import Union

import pandas as pd

from organon.ml.feature_selection.services.abstractions.base_feature_selecter import BaseFeatureSelecter


class BaseSupervisedFeatureSelecter(BaseFeatureSelecter, metaclass=abc.ABCMeta):
    """Base user service for supervised feature selection"""

    def __init__(self, data: pd.DataFrame, target: Union[pd.DataFrame, pd.Series]):
        super().__init__(data)
        self.target: Union[pd.DataFrame, pd.Series] = target

    @classmethod
    def _get_target_as_df(cls, target: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        target = target if isinstance(target, pd.DataFrame) else pd.DataFrame(target)
        return target
