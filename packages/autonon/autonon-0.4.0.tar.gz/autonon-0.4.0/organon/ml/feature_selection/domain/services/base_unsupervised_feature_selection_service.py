"""Includes BaseUnsupervisedFeatureSelectionService class."""
import abc
from typing import TypeVar, Generic

from organon.ml.feature_selection.domain.objects.base_selection_output import BaseSelectionOutput
from organon.ml.feature_selection.domain.objects.settings.base_unsupervised_feature_selection_settings import \
    BaseUnsupervisedFeatureSelectionSettings
from organon.ml.feature_selection.domain.services.base_feature_selection_service import BaseFeatureSelectionService

UnsupervisedFeatureSelectionSettingsType = TypeVar("UnsupervisedFeatureSelectionSettingsType",
                                                   bound=BaseUnsupervisedFeatureSelectionSettings)
FeatureSelectionOutputType = TypeVar("FeatureSelectionOutputType", bound=BaseSelectionOutput)


class BaseUnsupervisedFeatureSelectionService(
    Generic[UnsupervisedFeatureSelectionSettingsType, FeatureSelectionOutputType],
    BaseFeatureSelectionService[UnsupervisedFeatureSelectionSettingsType,
                                FeatureSelectionOutputType],
    metaclass=abc.ABCMeta):
    """Base service class for unsupervised feature selection services"""
