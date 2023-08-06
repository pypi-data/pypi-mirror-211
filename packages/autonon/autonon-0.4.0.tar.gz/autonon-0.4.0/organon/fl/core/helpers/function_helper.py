"""This module includes helper functions for retrieving function definition info."""
import inspect
from typing import Tuple, List, Dict, Any


def get_parameters(func) -> Tuple[List[str], Dict[str, Any]]:
    """
    Returns parameters of given func
    :param func:
    :return: tuple --> [parameter name list , parameters with default values as dictionary]
    """
    signature = inspect.signature(func)
    params_with_defaults = {key: value.default for key, value in signature.parameters.items()
                            if value.default != inspect.Parameter.empty}
    return list(signature.parameters.keys()), params_with_defaults
