"""This module includes helper functions and constants for parameter configurations."""
from typing import Dict

USE_CLASS_DEFAULT_STR = "NOT_SET"


def get_params(params: Dict) -> Dict:
    """filter parameters that wanted to be used as class default"""
    return {key: value for key, value in params.items() if value is not USE_CLASS_DEFAULT_STR}
