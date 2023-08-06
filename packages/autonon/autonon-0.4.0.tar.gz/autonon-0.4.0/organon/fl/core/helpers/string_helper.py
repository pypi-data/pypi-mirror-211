"""
This module keeps the helper functions for string type.
"""
import re

from organon.fl.core.extensions import string_extensions


def filter_non_alpha_numeric(string: str) -> str:
    """
    Returns alpha-numeric characters of the string.
    :param string: input string
    :return: alpha-numeric characters of the input string.
    """
    str_list = []
    for elem in string:
        if str.isalpha(elem) or str.isdigit(elem):
            str_list.append(elem)

    return ''.join(str_list)


def remove_single_character(string: str, char: str) -> str:
    """
    Removes a single character from the string
    :param string: string value
    :param char: character to remove
    :return: new string value without the input char
    """
    str_list = []
    for elem in string:
        if elem != char:
            str_list.append(elem)
    return ''.join(str_list)


def trim_double_quotes(string: str) -> str:
    """
    Trims the double quotes from a string.
    :param string: string value
    :return: trimmed string value
    """
    return remove_single_character(string, "\"")


def equals_ignoring_case(str1: str, str2: str) -> bool:
    """
    Compares if the two strings are equal with ignoring the case.
    :param str1: first string
    :param str2: second string
    :return: bool type to check if the two strings are equal
    """
    if str1 is None and str2 is None:
        return True

    if str1 is None or str2 is None:
        return False
    val = str1.upper() == str2.upper()
    return val


def to_upper_eng(text: str) -> str:
    """
    Returns the upper case representation of the string.
    :param text: text to change
    :return: text with uppercase letters
    """
    val = text.upper()
    return val


def to_lower_eng(text: str) -> str:
    """
    Returns the lower case representation of the string.
    :param text: text to change
    :return: text with lowercase letters
    """
    return text.lower()


def concatenate_all(*args) -> str:
    """
    Concatenates all arguments and returns as an output string.
    :param args: list of objects
    :return: concatenated objects
    """
    output_str: str = ""
    for string in args:
        if string is not None:
            output_str += string

    return output_str


def is_null_or_empty(string: str) -> bool:
    """
    Checks if the string is null or empty.
    :param string: string to be checked
    :return: bool type to check if the string is null or empty
    """
    if (string is None) or (string == ""):
        return True
    return False


def to_null_safe_string(obj: object) -> str:
    """
    Checks if the object is none.
    If so returns none.
    If not returns the string representation of the object.
    :param obj: object to be checked
    :return: string representation of the object
    """
    if obj is None:
        return None
    return str(obj)


def is_null_or_white_space(string: str) -> bool:
    """
    Checks if the string is null or consisting of just white spaces.
    :param string: string to be checked
    :return: bool type to check if the string null or consisting of just white spaces
    """
    return is_null(string) or is_string_just_white_space(string)


def is_null(string: str) -> bool:
    """
    Checks if the string is null.
    :param string: string to be checked
    :return: bool type to check if the string is null.
    """
    return string is None


def is_string_just_white_space(string: str) -> bool:
    """
    Checks if the string consists of just white spaces.
    :param string: string to be checked
    :return: true if the string consists of just white spaces.
    """
    return string.strip() == ""


def concatenate_with_pattern(pattern: str, connector: str, *args) -> str:
    """
    Concatenates all strings with pattern.
    :param pattern: pattern string
    :param connector: connector string
    :param args: list of strings
    :return: string representation of the concatenated strings with a pattern
    """
    if args is None:
        return ""
    concatenated_str: str = ""
    concatenated_str = concatenated_str.join([(pattern + connector).format(arg) for arg in args[:-1]] +
                                             [pattern.format(args[-1])])
    return concatenated_str


def concatenate_objects_with_pattern(pattern: str, connector: str, *args) -> str:
    """
    Concatenates all objects with pattern.
    :param pattern: pattern string
    :param connector: connector string
    :param args: list of objects to concatenate
    :return: string representation of the concatenated objects with a pattern
    """
    if args is None:
        return ""
    concatenated_str: str = ""
    string: str

    for arg in args:
        if arg is None:
            string = "null"
        else:
            string = string_extensions.effective_value(str(arg))
        concatenated_str += pattern.format(string)
        if arg != args[-1]:
            concatenated_str += connector
    return concatenated_str


def concatenate_objects_with_default_pattern(*args) -> str:
    """
    Concatenates all objects with a default pattern and connector.
    :param args: list of objects to concatenate
    :return: string representation of the concatenated objects with the default pattern
    """
    if args is None:
        return ""
    concatenated_str: str = ""
    string: str
    for arg in args:
        if arg is None:
            string = "null"
        else:
            string = string_extensions.effective_value(str(arg))
        concatenated_str += string
        if arg != args[:-1]:
            concatenated_str += ","
    return concatenated_str


camel_case_regex = re.compile(r'([a-z0-9])([A-Z])')


def camel_case_to_snake_case(camel_case_str: str):
    """Converts CamelCase string to snake_case."""
    return camel_case_regex.sub(r'\1_\2', camel_case_str).lower()


def replace_char(string_to_change: str, index: int, new_char: str) -> str:
    """Returns a new string with char at given index replaced by new_char"""
    return f"{string_to_change[:index]}{new_char}{string_to_change[index + 1:]}"
