"""Includes BaseUnsupervisedFeatureSelecter class"""
import abc

from organon.ml.feature_selection.services.abstractions.base_feature_selecter import BaseFeatureSelecter


class BaseUnsupervisedFeatureSelecter(BaseFeatureSelecter, metaclass=abc.ABCMeta):
    """Base user service for unsupervised feature selection"""
