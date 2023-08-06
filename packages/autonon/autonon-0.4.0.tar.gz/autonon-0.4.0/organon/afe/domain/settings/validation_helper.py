"""
This module has functions helping with implementation of afe_settings_validator
"""
from typing import List

import numpy as np

from organon.fl.core.exceptionhandling.known_exception import KnownException


def raise_or_add_exception(exc: Exception, exc_list: List[Exception], add_to_list: bool):
    """
    Raises an exception or adds it to list "exc_list" depending on "add_to_list" parameter
    :param exc: Exception to be raised or to be added to exc_list
    :type exc: Exception
    :param exc_list: The list to which exc will be appended if add_to_list is True
    :type exc_list: List[Exception]
    :param add_to_list: If true Exception exc will not be raised and will be added to exc_list
    :type add_to_list: bool
    """
    if add_to_list:
        exc_list.append(exc)
    else:
        raise exc


def check_required_attrs(obj, required_attrs: List[str], obj_str: str = "", exception_list: bool = False) \
        -> List[Exception]:
    """
    Given a list of attribute names of an object, this method checks if these attributes are not None.If there are None
    attributes an exception will be raised or a list of excepitons will be returned.
    :param obj:
    :param required_attrs: Names of attributes to be checked
    :type required_attrs: List[str]
    :param obj_str: A string to define the object instance
    :type obj_str: str
    :param exception_list: If True no exceptions will be raised and a list of excepitons will be returned.
    :type exception_list: bool
    :return:
    """
    exc_list = []
    for attr in required_attrs:
        if getattr(obj, attr) is None:
            exc = KnownException(f"{obj_str}.{attr} is not provided.")
            raise_or_add_exception(exc, exc_list, exception_list)
    return exc_list


def cast_attr(val: str, expected_type: type):
    """
    This function casts a string to types like int,float,bool,numpy.int64...
    :param val: String to be casted
    :type val: str
    :param expected_type: Type to which the string will be casted.
    :type expected_type: type
    :return: Casted value
    """
    if not isinstance(val, str) and expected_type != bool:
        return expected_type(val)

    if expected_type in [int, float, np.int64, np.short, np.float64, np.float32]:
        val = expected_type(val)
    elif expected_type == bool:
        if isinstance(val, bool):
            pass
        elif isinstance(val, str):
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            else:
                raise ValueError
        else:
            raise TypeError
    else:
        raise TypeError

    return val


def cast_to_np_type(val, np_type):
    """
    Casts a given value to numpy numerical types.
    :param val: Value to be casted
    :param np_type: Numpy type to which the value will be casted
    :return: Casted value.
    """
    if isinstance(val, float):  # prevent 5.5 from being casted to 5
        if np_type not in [np.float32, np.float64]:
            raise TypeError(f"Expected type is float. Got {type(val)}")

    np_types = [np.int64, np.short, np.float32, np.float64]
    if np_type in np_types:
        return np_type(val)

    raise TypeError("np_type should be one of numpy types!")
