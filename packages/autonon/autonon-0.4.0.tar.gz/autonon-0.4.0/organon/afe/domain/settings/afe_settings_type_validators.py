"""
This module has functions validating attribute types of the classes required for AfeModeliingSettings
"""
import inspect
from datetime import datetime
from enum import Enum
from typing import List, Dict, get_args, get_origin

import numpy as np

from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput
from organon.afe.domain.settings.base_afe_modelling_settings import BaseAfeModellingSettings
from organon.afe.domain.settings.base_afe_scoring_settings import BaseAfeScoringSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.validation_helper import cast_attr, raise_or_add_exception, cast_to_np_type
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers.date_helper import get_date_from_string

attr_basic_types = [str, int, float, bool, list, dict]
attr_np_types = [np.int64, np.short, np.float32, np.float64]


def attribute_types_validate(obj: object, attrs: Dict, obj_str: str = "", exception_list: bool = False) \
        -> List[Exception]:
    """
    Validates the types of attributes in the given object based on attribute types given in "attrs" dictionary.
    :param obj: Object instance to be validated
    :param attrs: A dictionary where keys are attribute names and values are expected types
    :param obj_str: A string that defines the given object
    :param exception_list: If true, this function will not raise an error and return a list of catched exceptions
    :return: Exception list.
    """
    exc_list = []
    for attr, expected_type in attrs.items():
        attr_val = getattr(obj, attr)
        val = __handle_type(attr_val, expected_type, f"{obj_str}.{attr}", exc_list, exception_list)
        setattr(obj, attr, val)
    return exc_list


def __handle_type(value, expected_type, definition: str, exc_list: List[Exception], add_to_list=False):
    if value is None:
        return None
    if inspect.isclass(expected_type):  # if expected_type is not a  "typing" type
        if expected_type in attr_basic_types or expected_type in attr_np_types:
            value = __handle_basic_or_np_type(value, expected_type, definition, exc_list, add_to_list=add_to_list)
        elif issubclass(expected_type, Enum):
            value = __handle_enum_type(value, expected_type, definition, exc_list, add_to_list=add_to_list)
        elif expected_type == datetime:
            value = __handle_datetime_type(value, definition, exc_list, add_to_list=add_to_list)
        else:
            exc_list.extend(_validate_types_for_class(value, expected_type, definition, exception_list=add_to_list))
    else:  # typing module types
        if get_origin(expected_type) == list:
            __handle_typing_list_type(value, expected_type, definition, exc_list, add_to_list=add_to_list)
        elif get_origin(expected_type) == dict:
            __handle_typing_dict_type(value, expected_type, definition, exc_list, add_to_list=add_to_list)
        else:
            raise NotImplementedError
    return value


def __handle_basic_or_np_type(value, expected_type, definition: str, exc_list: List[Exception], add_to_list=False):
    if expected_type in attr_basic_types or expected_type in attr_np_types:
        if not isinstance(value, expected_type):
            try:
                value = cast_to_basic_or_np(value, expected_type)
            except (ValueError, TypeError):
                exc = KnownException(
                    f"Type of '{definition}' is wrong. "
                    f"Expected: {expected_type} Got: {type(value)}(Value: {value})")
                raise_or_add_exception(exc, exc_list, add_to_list)
    return value


def __handle_datetime_type(value, definition: str, exc_list: List[Exception], add_to_list=False):
    if not isinstance(value, datetime):
        try:
            return get_date_from_string(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            exc = KnownException(
                f"Invalid date format or value in {definition}! Expected format:yyyy-mm-dd hh:mm:ss Got:{value}")
            raise_or_add_exception(exc, exc_list, add_to_list=add_to_list)
    return value


def __handle_typing_list_type(value, expected_type, definition: str, exc_list: List[Exception], add_to_list=False):
    list_element_type = get_args(expected_type)[0]
    if isinstance(value, list):
        for i in range(len(value)):  # pylint:disable=consider-using-enumerate
            elem = value[i]
            val = __handle_type(elem, list_element_type, f"{definition}[{i}]", exc_list, add_to_list=add_to_list)
            value[i] = val
    else:
        exc = KnownException(
            f"Type of '{definition}' is wrong. "
            f"Expected: List{list_element_type} Got: {type(value)}(Value: {value})")
        raise_or_add_exception(exc, exc_list, add_to_list)
    return value


def __handle_typing_dict_type(_dict, expected_type, definition: str, exc_list: List[Exception], add_to_list=False):
    key_type, value_type = get_args(expected_type)
    if isinstance(_dict, dict):
        for i, key in enumerate(list(_dict.keys())):
            value = _dict[key]
            new_key = __handle_type(key, key_type, f"{definition}.keys[{i}]", exc_list, add_to_list=add_to_list)
            new_value = __handle_type(value, value_type, f"{definition}[{key}]", exc_list, add_to_list=add_to_list)
            del _dict[key]
            _dict[new_key] = new_value
    else:
        exc = KnownException(
            f"Type of '{definition}' is wrong. "
            f"Expected: Dict[{key_type}, {value_type}] Got: {type(_dict)}(Value: {_dict})")
        raise_or_add_exception(exc, exc_list, add_to_list)
    return _dict


def cast_to_basic_or_np(value, value_type: type):
    """casts given value to given type if type in attr_basic_types or attr_np_types"""
    if value_type in attr_basic_types:
        return cast_attr(value, value_type)
    if value_type in attr_np_types:
        return cast_to_np_type(value, value_type)
    raise NotImplementedError


def __handle_enum_type(value, expected_enum_type, definition: str, exc_list: List[Exception], add_to_list=False):
    if isinstance(value, expected_enum_type):
        return value
    valid_values = [e.name for e in expected_enum_type]
    if value not in valid_values:
        exc = KnownException(
            f"Invalid value for enum '{expected_enum_type}' in {definition}. "
            f"Expected one of: {str(valid_values)} Got: {value}")
        raise_or_add_exception(exc, exc_list, add_to_list)
    else:
        value = expected_enum_type[value]
    return value


def _validate_types_for_class(obj, expected_type, obj_str: str, exception_list: bool = False) -> List[Exception]:
    """
    Validates the types of attributes in the given object

    :param obj: Object to be validated
    :param expected_type: Expected type for object
    :param obj_str: A string to define the object
    :type obj_str: str
    :param exception_list: If true, this function will not raise an error and return a list of catched exceptions
    :type exception_list: bool
    :return: Exception list
    """
    exc_list = []
    if not isinstance(obj, expected_type):
        exc = KnownException(
            f"Type of '{obj_str}' is wrong. "
            f"Expected: {expected_type} Got: {type(obj)}(Value: {obj})")
        raise_or_add_exception(exc, exc_list, exception_list)
    else:
        if issubclass(expected_type, BaseAfeModellingSettings):
            exc_list = validate_types_modelling_settings(obj, exception_list=exception_list)
        elif issubclass(expected_type, RecordSource):
            exc_list = validate_types_record_source(obj, obj_str, exception_list)
        elif hasattr(obj, "ATTR_DICT"):
            exc_list = validate_types_for_obj_with_attr_dict(obj, obj_str, exception_list)
        else:
            raise NotImplementedError(f"No type validation functions for given class: {expected_type}")

    return exc_list


def validate_types_for_obj_with_attr_dict(obj, obj_str: str = "", exception_list: bool = False) -> List[Exception]:
    """
    Validate types of attributes in obj instance using its ATTR_DICT attribute
    :param obj_str:
    :param obj:
    :param exception_list: If true, no exceptions will be raised and a list of catched exceptions will be returned
    :type exception_list: bool
    :return: Exception list
    """
    return attribute_types_validate(obj, obj.ATTR_DICT, obj_str, exception_list=exception_list)


def validate_types_modelling_settings(obj: BaseAfeModellingSettings, exception_list: bool = False) -> List[Exception]:
    """
    Validate types of attributes in AfeModellingSettings instance
    :param obj:
    :type obj: BaseAfeModellingSettings
    :param exception_list: If true, no exceptions will be raised and a list of catched exceptions will be returned
    :type exception_list: bool
    :return: Exception list
    """
    exc_list = validate_types_for_obj_with_attr_dict(obj, "", exception_list=exception_list)

    if obj.algorithm_settings is not None:
        exc_list.extend(validate_types_for_obj_with_attr_dict(obj.algorithm_settings, "algorithm_settings",
                                                              exception_list=exception_list))
    return exc_list


def validate_types_record_source(obj: RecordSource, obj_str: str = "record_source",
                                 exception_list: bool = False) -> List[Exception]:
    """
    Validate types of attributes in TargetRecordSource instance
    :param RecordSource obj:
    :param str obj_str: A string to define the instance of object
    :param bool exception_list: If true, no exceptions will be raised and a list of catched exceptions will be returned
    :return: Exception list
    """
    exc_list = []
    if obj.get_type() == RecordSourceType.DATABASE:
        exc_list.extend(validate_types_for_obj_with_attr_dict(obj.source, obj_str=f"{obj_str}.source",
                                                              exception_list=exception_list))
    return exc_list


def validate_types_scoring_settings(obj: BaseAfeScoringSettings, exception_list: bool = False) -> List[Exception]:
    """
    Validate types of attributes in AfeScoringSettings instance
    :param obj:
    :type obj: PAfeScoringSettings
    :param exception_list: If true, no exceptions will be raised and a list of catched exceptions will be returned
    :type exception_list: bool
    :return: Exception list
    """
    exc_list = []
    attrs = obj.ATTR_DICT.copy()
    attrs.pop("model_output")
    exc_list.extend(attribute_types_validate(obj, attrs, exception_list=exception_list))
    if obj.model_output is not None and not isinstance(obj.model_output, BaseAfeModelOutput):
        exc = KnownException("scoring_settings.model_output is not an instance of BaseAfeModelOutput")
        raise_or_add_exception(exc, exc_list, add_to_list=exception_list)

    return exc_list
