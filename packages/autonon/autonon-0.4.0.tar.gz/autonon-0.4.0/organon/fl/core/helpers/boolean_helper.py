"""
This module keeps the helper functions for boolean type.
"""


def to_int(bool_input: bool) -> int:
    """
    Convert boolean to int.
    True => 1
    False => 0
    :param bool_input: input boolean
    :return: integer representation of the boolean
    """
    if bool_input:
        return 1
    return 0


def from_int(num: int) -> bool:
    """
    Converts int to boolean.
    1 => True
    0 => False
    :param num: input integer
    :return: boolean representation of the integer
    """
    if num == 1:
        return True
    return False
