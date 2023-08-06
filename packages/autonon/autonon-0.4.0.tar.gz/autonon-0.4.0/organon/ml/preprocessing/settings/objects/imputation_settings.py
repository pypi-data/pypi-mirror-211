"""Includes ImputationSettings class."""
from dataclasses import dataclass
from typing import Union, List

from organon.ml.preprocessing.settings.enums.imputer_type import ImputerType


@dataclass
class ImputationSettings:
    """Settings for Imputation service"""
    numeric_data_method: ImputerType
    categorical_data_method: ImputerType
    n_missing_values: Union[int, float, None]
    c_missing_values: Union[int, float, str, None]
    n_strategy: str
    c_strategy: str
    n_fill_value: Union[float, int]
    c_fill_value: Union[str, float, int]
    included_columns: List[str] = None
