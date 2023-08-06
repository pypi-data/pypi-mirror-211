"""
This module has functions helping with implementation of afe_settings_reader
"""
import inspect

from typing import List, Dict, Type, get_args, get_origin
from typing import TypeVar

# pylint: disable=invalid-name
T = TypeVar('T')


def get_list_of_objects_from_list_of_dicts(_list: List[Dict], given_class: Type[T]) -> List[T]:
    """
    Given a list of dictionaries storing object attributes and values,this method returns a list of objects of
    type "given_class"

    :param _list: List of dictionaries storing object attributes and their values
    :type _list: List[Dict]
    :param given_class: Type of objects to created and returned in a list
    :return: List[T]
    """
    if isinstance(_list, list):
        ret_list = []
        for obj in _list:
            if not isinstance(obj, given_class) and isinstance(obj, dict):
                ret_list.append(given_class(**obj))
            else:
                ret_list.append(obj)
        return ret_list
    return None


def set_attrs_from_dict(_dict: Dict, obj):
    """
    Set simple type attributes of a given object from a given dictionary storing attributes and their values.
    :param _dict:
    :type _dict: Dict
    :param obj:
    :return:
    """
    for attr in obj.__dict__:
        if attr in _dict:
            _type = type(_dict[attr])
            if _type in [str, int, bool, float, list]:
                setattr(obj, attr, _dict[attr])


def set_defaults_from_dict(obj, defaults_dict: Dict):
    """
    Set attribute values of an object recursively if they are None.
    :param obj: Object to set the attributes
    :param defaults_dict: A dictionary storing the values for attributes
    :type defaults_dict: Dict
    """
    for attr in defaults_dict:
        if attr in obj.__dict__:
            dict_val = defaults_dict[attr]
            obj_val = getattr(obj, attr)
            if obj_val is None:
                if not isinstance(dict_val, dict):
                    setattr(obj, attr, dict_val)
                else:
                    if hasattr(obj, "ATTR_DICT") and obj.ATTR_DICT[attr] == dict:
                        setattr(obj, attr, dict_val)
            elif isinstance(dict_val, dict):
                if isinstance(obj_val, dict):
                    set_defaults_from_dict_to_dict(obj_val, dict_val)
                else:
                    set_defaults_from_dict(obj_val, dict_val)


def set_defaults_from_dict_to_dict(var_dict: Dict, defaults_dict: Dict) -> Dict:
    """
    Assign default values from defaults_dict to var_dict
    :param var_dict: Dictionary to be set by defaults
    :param defaults_dict: Dictionary for default values
    :return: set dictionary
    """

    if var_dict is None:
        return defaults_dict

    for key in defaults_dict:
        var_dict.setdefault(key, defaults_dict[key])

    return var_dict


def setattr_if_none(obj, attr, val):
    """Sets object attribute value to if it is None"""
    if getattr(obj, attr) is None:
        setattr(obj, attr, val)


def get_val_from_kwargs(value, target_type):
    """If values is of target_type, returns value. Else if it is a dict, generates target_type instance from dict. Else
    returns value."""
    if isinstance(value, target_type):
        return value
    if isinstance(value, dict):
        return target_type(**value)
    return value


def get_values_from_kwargs(obj, attr_dict: dict, kwargs_dict: dict, ignored_attrs: List[str] = None):
    """
    Initializes obj using given attributes and values

    :param obj: obj to be initialized
    :param dict attr_dict: map of attribute names and types
    :param dict kwargs_dict: map of attribute values
    :param ignored_attrs: attributes to ignore
    """
    for attr, value in kwargs_dict.items():
        if ignored_attrs is not None and attr in ignored_attrs:
            continue
        if attr not in attr_dict:
            raise ValueError(f"{type(obj)} class has no attribute named '{attr}'")
        attr_type = attr_dict[attr]
        if attr_type != type(value):
            if isinstance(value, dict):
                value = attr_type(**value)
            elif isinstance(value, list):
                if not inspect.isclass(attr_type) and get_origin(attr_type) == list:
                    value = get_list_of_objects_from_list_of_dicts(value, get_args(attr_type)[0])
        setattr(obj, attr, value)
