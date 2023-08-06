"""Includes helper functions to use in user input services"""
from typing import Type, TypeVar

from organon.fl.core.exceptionhandling.known_exception import KnownException

T = TypeVar("T")


def get_default_if_none(value: T, default_value: T) -> T:
    """Returns a default value if the value is None, else returns the value"""
    return value if value is not None else default_value


def get_enum(enum_str: str, enum_class: Type[T]) -> T:
    """Converts string to enum """
    if enum_str is None:
        return None

    valid_values = {e.name.upper(): e for e in enum_class}

    if enum_str.upper() in valid_values:
        return valid_values[enum_str.upper()]

    raise KnownException(
        f"Invalid value for enum '{enum_class.__name__}'."
        f"Expected one of: {str(list(valid_values.keys()))} Got: '{enum_str}'")
