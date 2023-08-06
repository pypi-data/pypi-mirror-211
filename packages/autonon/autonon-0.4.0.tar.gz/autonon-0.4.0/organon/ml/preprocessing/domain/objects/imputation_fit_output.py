"""Includes ImputationFitOutput class."""
from typing import Union, Dict

# noinspection PyUnresolvedReferences
from sklearn.experimental import enable_iterative_imputer  # pylint: disable=unused-import
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer


class ImputationFitOutput:
    """Output of imputation fitting process"""

    def __init__(self):
        self.categorical_imputer: Dict[str, SimpleImputer] = None
        self.numerical_imputer: Union[Dict[str, SimpleImputer], IterativeImputer] = None
