"""Includes BaseSupervisedFeatureSelectionService class."""
import abc
from typing import TypeVar, Generic

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_selection.domain.objects.base_selection_output import BaseSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.base_supervised_feature_selection_settings import \
    BaseSupervisedFeatureSelectionSettings
from organon.ml.feature_selection.domain.services.base_feature_selection_service import BaseFeatureSelectionService

SupervisedFeatureSelectionSettingsType = TypeVar("SupervisedFeatureSelectionSettingsType",
                                                 bound=BaseSupervisedFeatureSelectionSettings)
FeatureSelectionOutputType = TypeVar("FeatureSelectionOutputType", bound=BaseSelectionOutput)


class BaseSupervisedFeatureSelectionService(Generic[SupervisedFeatureSelectionSettingsType, FeatureSelectionOutputType],
                                            BaseFeatureSelectionService[SupervisedFeatureSelectionSettingsType,
                                                                        FeatureSelectionOutputType],
                                            metaclass=abc.ABCMeta):
    """Base service class for supervised feature selection services"""

    @classmethod
    def _get_target_data_as_series_of_numbers(cls, settings: SupervisedFeatureSelectionSettingsType):
        if settings.target_type == TargetType.BINARY:
            label_encoder = LabelEncoder()
            label_encoder.fit(settings.target)
            return pd.Series(label_encoder.transform(settings.target[settings.target.columns[0]]))
        return settings.target[settings.target.columns[0]]
