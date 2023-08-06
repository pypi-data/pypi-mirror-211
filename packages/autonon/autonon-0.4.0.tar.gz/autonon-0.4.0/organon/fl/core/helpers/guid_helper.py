"""
This module keeps the helper functions for guid type.
"""
import uuid


def new_guid(max_length: int = None) -> str:
    """
    Returns a uuid value as a string.
    Max_length parameter limits the maximum length of the returned string.
    :param max_length: maximum length of the uuid value
    :return: uuid value as a string
    """
    if max_length is None:
        return str(uuid.uuid4())
    if 0 < max_length < 36:
        return str(uuid.uuid4()).replace("-", "")[:max_length]
    return ""
