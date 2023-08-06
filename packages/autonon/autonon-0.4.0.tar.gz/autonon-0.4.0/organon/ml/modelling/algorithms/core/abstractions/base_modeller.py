"""Includes BaseModeller class."""
import abc
from typing import Any, Dict, Union

import numpy as np
import pandas as pd
from sklearn import clone

# THIS CLASS IS THE BASE CLASS FOR OUR REGRESSORS AND CLASSIFIERS. ALL OF THESE REGRESSORS AND CLASSIFIERS SHOULD BE
# USABLE IN HYPERPARAMETER OPTIMIZATION MODULE. THAT MODULE REQUIRES SOME MODULES TO BE DEFINED IN
# ESTIMATOR(MODELLER AS WE CALL IT) CLASSES AND THERE ARE SOME REQUIREMENTS ON __init__ METHOD AND PARAMETERS TOO.
# THESE REQUIREMENTS EXIST BECAUSE HYPERPARAMETER OPTIMIZATION MODULE USES PIPELINE, GRIDSEARCHCV etc. FROM SKLEARN
# PACKAGE AND OUR CLASSIFIERS AND REGRESSORS SHOULD BE ABLE TO BE USED WITH THESE.
# CHECK REQUIREMENTS FOR SKLEARN ESTIMATORS IN https://scikit-learn.org/stable/developers/develop.html
from organon.ml.modelling.algorithms.core.enums.modeller_type import ModellerType


class BaseModeller(metaclass=abc.ABCMeta):
    """Base class for all modellers"""

    # REQUIRED FOR SKLEARN GridSearch. Set to classifier, regressor etc. in child classes
    # https://scikit-learn.org/stable/developers/develop.html#estimator-types
    _estimator_type = None

    def __init__(self, **params):
        # See __init__ method requirements in https://scikit-learn.org/stable/developers/develop.html#instantiation
        # DO NOT OVERRIDE __INIT__ IN CHILD CLASSES. THIS __init__ IN THIS BASE CLASS IS WRITTEN IN A WAY THAT NEW
        # MODELLER CLASSES DO NOT HAVE TO DECLARE AN __init__ WHICH WILL ABIDE SKLEARN RULES. YOU SHOULD ONLY IMPLEMENT
        # _get_params_with_defaults METHOD WHICH WILL RETURN A DICTIONARY OF MODELLER PARAMETERS AND
        # THEIR DEFAULT VALUES. __init__ IMPLEMENTATION IN THIS CLASS WILL HANDLE FURTHER REQUIREMENTS

        self.set_params(**self._get_params_with_defaults())
        self.set_params(**params)

    def fit(self, train_data: Union[pd.DataFrame, np.ndarray], target_data: Union[pd.DataFrame, pd.Series, np.ndarray],
            **kwargs):
        """Fits model and returns self"""
        # THIS METHOD IS REQUIRED FOR SKLEARN ESTIMATORS. DO NOT CHANGE ITS SIGNATURE AND DO NOT DIRECTLY OVERRIDE THIS
        # TO IMPLEMENT FITTING. OVERRIDE _fit ABSTRACT METHOD INSTEAD.
        if isinstance(train_data, np.ndarray):
            train_data = pd.DataFrame(train_data)
        if isinstance(target_data, np.ndarray):
            target_data = pd.Series(target_data)
        self.train_data_columns_ = train_data.columns.tolist()  # pylint: disable=attribute-defined-outside-init
        self._fit(train_data, target_data, **kwargs)
        self.fitted_ = True  # pylint: disable=attribute-defined-outside-init
        return self

    @abc.abstractmethod
    def _fit(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series], **kwargs):
        """Fits the model"""

    def predict(self, data: Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
        """Predicts using fitted model and returns predictions"""
        # THIS METHOD IS REQUIRED FOR SKLEARN ESTIMATORS. DO NOT CHANGE ITS SIGNATURE AND DO NOT DIRECTLY OVERRIDE THIS
        # TO IMPLEMENT FITTING. OVERRIDE _predict ABSTRACT METHOD INSTEAD.
        self._check_is_fitted()
        if isinstance(data, np.ndarray):
            data = pd.DataFrame(data)
        return self._predict(data)

    def is_fitted(self) -> bool:
        """Returns True if model is fitted"""
        return hasattr(self, "fitted_") and self.fitted_

    def _check_is_fitted(self):
        """Raise error if modeller is not fitted yet"""
        if not self.is_fitted():
            raise ValueError("Modeller not fitted yet")

    @abc.abstractmethod
    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prediction using fitted model"""

    def score(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series],
              sample_weight=None) -> float:
        """Returns a score value after predicting train_data and comparing it with actual target_data"""
        # THIS METHOD IS REQUIRED FOR SKLEARN GridSearchCV ETC.
        # DO NOT CHANGE ITS SIGNATURE AND DO NOT DIRECTLY OVERRIDE THIS
        # TO IMPLEMENT FITTING. OVERRIDE _score ABSTRACT METHOD INSTEAD.
        self._check_is_fitted()
        return self._score(train_data, target_data, sample_weight=sample_weight)

    @abc.abstractmethod
    def _score(self, train_data: pd.DataFrame, target_data: Union[pd.DataFrame, pd.Series],
               sample_weight=None) -> float:
        """Returns a score value after predicting train_data and comparing it with actual target_data"""

    @abc.abstractmethod
    def _get_params_with_defaults(self) -> Dict[str, Any]:
        """Returns modeller parameter names and their default values"""

    def get_params(self, deep=True):
        """Returns dictionary of parameters and their values"""
        # pylint: disable=unused-argument
        # THIS METHOD IS REQUIRED FOR SKLEARN ESTIMATORS
        # https://scikit-learn.org/stable/developers/develop.html#get-params-and-set-params
        out = {}
        for key in self._get_params_with_defaults():
            value = getattr(self, key)
            out[key] = value
        return out

    def set_params(self, **params):
        """Set modeller parameter values"""
        # THIS METHOD IS REQUIRED FOR SKLEARN ESTIMATORS
        # https://scikit-learn.org/stable/developers/develop.html#get-params-and-set-params
        if not params:
            return self
        valid_params = self._get_params_with_defaults()
        for param, value in params.items():
            if param not in valid_params:
                raise ValueError(
                    f"Invalid parameter {param} for estimator {self}. "
                    "Check the list of available parameters "
                    "with `estimator.get_params().keys()`."
                )
            setattr(self, param, value)
        return self

    def clone(self):
        """Construct and return a new unfitted estimator with the same parameters."""
        return clone(self)

    @property
    @abc.abstractmethod
    def modeller_type(self) -> ModellerType:
        """Returns type of modeller"""
