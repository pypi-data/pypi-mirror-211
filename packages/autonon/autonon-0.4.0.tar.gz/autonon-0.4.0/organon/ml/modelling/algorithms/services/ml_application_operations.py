"""
This module includes MLApplicationOperations class.
"""
import threading

import organon
from organon.common.helpers import dev_mode_helper
from organon.fl.core.iocutil import ioc_helper
from organon.fl.core.iocutil.ioc_registration_item import IocRegistrationItem
from organon.fl.generic.interaction.fl_initializer import FlInitializer
from organon.ml.modelling.algorithms.classifiers.gam_classifier import GamClassifier
from organon.ml.modelling.algorithms.classifiers.gbm_classifier import GBMClassifier
from organon.ml.modelling.algorithms.classifiers.lightgbm_classifier import LightGBMClassifier
from organon.ml.modelling.algorithms.classifiers.logistic_regression_classifier import LogisticRegressionClassifier
from organon.ml.modelling.algorithms.classifiers.multi_layer_perceptron_classifier import MultiLayerPerceptronClassifier
from organon.ml.modelling.algorithms.classifiers.rf_classifier import RFClassifier
from organon.ml.modelling.algorithms.classifiers.xgboost_classifier import XGBoostClassifier
from organon.ml.modelling.algorithms.core.abstractions.base_regressor import BaseModeller
from organon.ml.modelling.algorithms.core.enums.modeller import Modeller
from organon.ml.modelling.algorithms.regressors.gam_regressor import GamRegressor
from organon.ml.modelling.algorithms.regressors.gbm_regressor import GBMRegressor
from organon.ml.modelling.algorithms.regressors.lasso_regressor import LassoRegressor
from organon.ml.modelling.algorithms.regressors.lightgbm_regressor import LightGBMRegressor
from organon.ml.modelling.algorithms.regressors.multi_layer_perceptron_regressor import MultiLayerPerceptronRegressor
from organon.ml.modelling.algorithms.regressors.rf_regressor import RFRegressor
from organon.ml.modelling.algorithms.regressors.ridge_regressor import RidgeRegressor
from organon.ml.modelling.algorithms.regressors.xgboost_regressor import XGBoostRegressor


class MLApplicationOperations:
    """
    MLApplicationOperations
    """

    APPLICATION_INITIALIZED = False
    __INITIALIZATION_LOCK = threading.Lock()

    @classmethod
    def initialize_app(cls):
        """Initializes application."""
        with MLApplicationOperations.__INITIALIZATION_LOCK:
            if not MLApplicationOperations.APPLICATION_INITIALIZED:
                cls._on_init()
                MLApplicationOperations.APPLICATION_INITIALIZED = True

    @classmethod
    def _on_init(cls):
        cls._initialize_fl()
        cls.register_types()

    @classmethod
    def _initialize_fl(cls):
        FlInitializer.application_initialize()

    @classmethod
    def init_dev_mode(cls, log_to_console: bool = True, log_file: str = "application.log"):
        """Initializes development mode."""
        dev_mode_helper.init_dev_mode(organon.ml.__name__, log_to_console=log_to_console, log_file=log_file)

    @classmethod
    def register_types(cls):
        """
        Registers ioc items
        """
        ioc_helper.register_type(IocRegistrationItem(Modeller.LOGISTIC_REGRESSION_CLASSIFIER.name,
                                                     BaseModeller, LogisticRegressionClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.GAM_CLASSIFIER.name,
                                                     BaseModeller, GamClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.GBM_CLASSIFIER.name,
                                                     BaseModeller, GBMClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.LIGHTGBM_CLASSIFIER.name,
                                                     BaseModeller, LightGBMClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.RF_CLASSIFIER.name,
                                                     BaseModeller, RFClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.XGBOOST_CLASSIFIER.name,
                                                     BaseModeller, XGBoostClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.MULTI_LAYER_PERCEPTRON_CLASSIFIER.name,
                                                     BaseModeller, MultiLayerPerceptronClassifier))

        ioc_helper.register_type(IocRegistrationItem(Modeller.GAM_REGRESSOR.name,
                                                     BaseModeller, GamRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.RIDGE.name,
                                                     BaseModeller, RidgeRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.LASSO.name,
                                                     BaseModeller, LassoRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.GBM_REGRESSOR.name,
                                                     BaseModeller, GBMRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.LIGHTGBM_REGRESSOR.name,
                                                     BaseModeller, LightGBMRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.RANDOM_FOREST_REGRESSOR.name,
                                                     BaseModeller, RFRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.XGBOOST_REGRESSOR.name,
                                                     BaseModeller, XGBoostRegressor))

        ioc_helper.register_type(IocRegistrationItem(Modeller.MULTI_LAYER_PERCEPTRON_REGRESSOR.name,
                                                     BaseModeller, MultiLayerPerceptronRegressor))
