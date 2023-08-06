"""
This module keeps the helper functions for dictionary type.
"""
from typing import Dict, TypeVar
import logging

from organon.fl.core.helpers import string_helper

T1 = TypeVar('T1')
V1 = TypeVar('V1')


def add_if_key_not_exist(key: T1, value: V1, dict_to_insert: Dict):
    """
    Adds a key-value pair if the key not exists. Raises TypeError otherwise.
    :param key: key
    :param value: value
    :param dict_to_insert: dict to insert the key-value pair
    :return: Nothing
    """
    if key not in dict_to_insert:
        dict_to_insert[key] = value
    else:
        logging.error("Key is already defined in the dictionary!")
        raise TypeError


def camel_case_keys_to_snake_case(_dict: Dict):
    """Converts keys from CamelCase to snake_case """
    new_dict = {}
    for key in _dict:
        val = _dict[key]
        newkey = string_helper.camel_case_to_snake_case(key)
        if isinstance(val, dict):
            new_dict[newkey] = camel_case_keys_to_snake_case(_dict[key])
        else:
            new_dict[newkey] = _dict[key]

    return new_dict
