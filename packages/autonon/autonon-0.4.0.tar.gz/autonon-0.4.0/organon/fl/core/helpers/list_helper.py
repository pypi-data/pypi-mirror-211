"""
This module keeps the helper functions for list type.
"""
import bisect
from typing import TypeVar, List

T1 = TypeVar('T1')


def binary_search(obj_list: List[T1], value: T1) -> int:
    """
    Returns index of the given value in given sorted list. Returns -1 if not found.
    :param value: value to be searched in list
    :param obj_list: list of objects
    :return: index of given value in list
    """
    search_index = bisect.bisect_left(obj_list, value)
    if search_index != len(obj_list) and obj_list[search_index] == value:
        return search_index
    return -1


def is_null_or_empty(obj_list: List[T1]) -> bool:
    """
    Checks if the object list is null or empty.
    :param obj_list: list of objects
    :return: boolean type to check if the object list is null or empty
    """
    return obj_list is None or len(obj_list) == 0


def is_null(obj: List[T1]) -> bool:
    """
    Checks if the object list is null.
    :param obj: list of objects
    :return: boolean type to check if the object list is null
    """
    return obj is None
