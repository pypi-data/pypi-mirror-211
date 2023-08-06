"""
This module includes methods to serialize objects.
"""
from enum import Enum
from typing import Dict

import numpy as np

from organon.fl.core.helpers import object_helper


def serialize_to_file(obj, filepath: str, secret_key: str = None):
    """
    Binary serialization of object to given file

    :returns : secret key used in encryption of pickled data. should be saved for deserialization
    """

    with open(filepath, "wb") as file:
        byte_val, secret_key = object_helper.get_encrypted_binary(obj, secret_key=secret_key)
        file.write(byte_val)
    return secret_key


def deserialize_from_file(filepath: str, secret_key: str):
    """Binary deserialization object from file."""
    with open(filepath, "rb") as readfile:
        obj = object_helper.get_object_from_encrypted_binary(readfile.read(), secret_key)
    return obj


def normalize_dictionary_for_json_conversion(_d: Dict):
    """Normalizes dictionary keys to become usable with json.dump"""
    type_map = {
        float: [float, np.float, np.float32],
        int: [int, np.int, np.int16, np.int32]
    }
    new_d = {}
    for key in _d:
        val = _d[key]
        val_type = type(val)

        if isinstance(val, dict):
            val = normalize_dictionary_for_json_conversion(val)
        elif val_type in type_map[float]:
            val = float(val)
        if isinstance(key, Enum):
            new_d[key.name] = val
        else:
            new_d[str(key)] = val

    return new_d
