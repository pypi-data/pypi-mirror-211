"""
This module keeps functions performing the string operations.
"""


def get_bytes(string: str) -> bytearray:
    """
    Returns the string as a byte array.
    :param string: str
    :return: bytearray
    """
    return bytearray(string, "utf-8")


def is_alpha_numeric(string: str) -> bool:
    """
    Checks if the string is an alpha-numeric string.
    :param string: str
    :return: bool
    """
    return string.isalnum()


def is_word(string: str) -> bool:
    """
    Checks if the string is an alphabetic string.
    :param string: str
    :return: bool
    """
    return string.isalpha()


def is_number(string: str) -> bool:
    """
    Checks if the string is an numeric string.
    :param string: str
    :return: bool
    """
    return string.isnumeric()


def get_db_column_name_compatible_string(input_str: str, max_length: int) -> str:
    """
    Filters the input string according to the valid char list and returns it.
    :param input_str: str
    :param max_length: int
    :return: str
    """
    i: int = 0
    tot_chars: int = 0
    valid_char_list: str = "0123456789abcdefghjklmnoprqstuxwvyzABCDEFGHJKLMNOPRQSTUXWVYZ_"
    output_str: str = ""

    while tot_chars < max_length and i < len(input_str):

        char: str = input_str[i]
        if char in valid_char_list:
            output_str += char
            tot_chars += 1

        i += 1

    return output_str


def is_empty(string: str) -> bool:
    """
    Checks if the string is empty.
    :param string: str
    :return: bool
    """
    return not string


def remove_single_character(string: str, char: str) -> str:
    """
    Replaces a character from a string and returns it.
    :param string: str
    :param char: str
    :return: str
    """
    return string.replace(char, "")


def contains_white_space(string: str) -> bool:
    """
    Checks if the string contains white space.
    :param string: str
    :return: bool
    """
    return " " in string


def nullable_length(input_str: str = None) -> str:
    """
    Checks the input string is none or empty.
    If it is none or empty string, return "null", if it is not returns the length of the string.
    :param input_str: str
    :return: str
    """
    if input_str is None or input_str == "":
        return "null"
    return str(len(input_str))


def effective_value(input_str: str = None) -> str:
    """
    Checks the input string is none or empty.
    If it is none returns "null"
    If it is empty returns "empty"
    If both of them are not correct return the input string.
    :param input_str: str
    :return: str
    """
    if input_str is None:
        return "null"
    if input_str.strip() == "":
        return "empty"
    return input_str


def equals_ignoring_case(input_str: str, compared_string: str) -> bool:
    """
    Compares the two strings with ignoring the case.
    :param input_str: str
    :param compared_string: str
    :return: bool
    """
    if input_str is None and compared_string is None:
        return True

    if input_str is None or compared_string is None:
        return False

    val = input_str.upper() == compared_string.upper()

    return val


def to_upper_eng(input_str: str) -> str:
    """
    Returns the upper case representation of the string.
    :param input_str: str
    :return: str
    """
    val = input_str.upper()
    return val


def to_lower_eng(input_str: str) -> str:
    """
    Returns the lower case representation of the string.
    :param input_str: str
    :return: str
    """
    val = input_str.lower()
    return val
