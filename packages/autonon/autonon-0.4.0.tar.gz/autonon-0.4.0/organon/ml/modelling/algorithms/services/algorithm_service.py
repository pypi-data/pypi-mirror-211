"""Includes AlgorithmService class."""
from typing import Union

from organon.fl.core.iocutil import ioc_helper
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.modelling.algorithms.core.abstractions.base_classifier import BaseClassifier
from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller
from organon.ml.modelling.algorithms.core.abstractions.base_regressor import BaseRegressor
from organon.ml.modelling.algorithms.core.enums.modeller import Modeller
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType
from organon.ml.modelling.algorithms.services.ml_application_operations import MLApplicationOperations


class AlgorithmService:
    """Service for modelling algorithms"""

    def __init__(self):
        self._initialize_ml()

    @classmethod
    def _initialize_ml(cls):
        MLApplicationOperations.initialize_app()

    @classmethod
    def get_regressor(cls, regressor_type: Union[str, Modeller], **kwargs) -> BaseRegressor:
        """Returns regressor for given regressor type"""
        if isinstance(regressor_type, str):
            regressor_type = get_enum(regressor_type, Modeller)
        if regressor_type.get_modeller_type() != ModellerType.REGRESSOR:
            raise ValueError("Given modeller is not a regression modeller")
        regressor = ioc_helper.resolve(BaseModeller, regressor_type.name, init_args=kwargs)
        return regressor

    @classmethod
    def get_classifier(cls, classifier_type: Union[str, Modeller], **kwargs) -> BaseClassifier:
        """Returns classifier for given classifier type"""
        if isinstance(classifier_type, str):
            classifier_type = get_enum(classifier_type, Modeller)
        if classifier_type.get_modeller_type() != ModellerType.CLASSIFIER:
            raise ValueError("Given modeller is not a classification modeller")
        classifier = ioc_helper.resolve(BaseModeller, classifier_type.name, init_args=kwargs)
        return classifier

    @classmethod
    def get_modeller(cls, modeller_type: Union[str, Modeller], **kwargs) -> BaseModeller:
        """Returns modeller for given modeller type"""
        if isinstance(modeller_type, str):
            modeller_type = get_enum(modeller_type, Modeller)
        modeller = ioc_helper.resolve(BaseModeller, modeller_type.name, init_args=kwargs)
        return modeller
