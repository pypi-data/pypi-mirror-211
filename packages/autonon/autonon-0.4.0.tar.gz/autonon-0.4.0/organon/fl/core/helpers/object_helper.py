"""
This module keeps the helper functions for object type.
"""
import codecs
import inspect
import pickle  # nosec
import zlib
from typing import Tuple

from organon.fl.security.helpers.encryption_helper import EncryptionHelper


class DecompressionError(Exception):
    """Error raised when decompression fails"""


def get_encrypted_binary(obj, secret_key: str = None, compress: bool = False) -> Tuple[bytes, str]:
    """Convert object to binary"""
    bin_val = pickle.dumps(obj)
    # compression should be done before encrypting, otherwise proper compression cannot be done
    # and size of bytes object might even increase
    if compress:
        bin_val = _compress_bytes(bin_val)
    return EncryptionHelper.encrypt_bytes(bin_val, secret_key=secret_key)


def get_encrypted_binary_str(obj, secret_key: str):
    """Converts object to bytes and then base64 string"""
    objbin, _ = EncryptionHelper.encrypt_bytes(obj, secret_key)
    bytestr = codecs.encode(objbin, "base64").decode("utf-8")
    return bytestr


def get_object_from_encrypted_binary(binary: bytes, secret_key: str, is_compressed: bool = False):
    """Converts bytes to object"""
    bin_val = EncryptionHelper.decrypt_bytes(binary, secret_key)
    if is_compressed:
        try:
            bin_val = _decompress_bytes(bin_val)
        except zlib.error as exc:
            raise DecompressionError from exc
    return pickle.loads(bin_val)  # nosec


def get_object_from_encrypted_binary_str(string: str, secret_key: str):
    """Converts base64 encoded bytes to object"""
    encoded = string.encode("utf-8")
    decoded = codecs.decode(encoded, "base64")
    unpickled = pickle.loads(EncryptionHelper.decrypt_bytes(decoded, secret_key))  # nosec
    return unpickled


def get_attribute_dict(obj, with_class_attrs: bool = False):
    """Returns a dictionary where keys are object attributes and values are attribute values"""

    if not with_class_attrs:
        return obj.__dict__

    members = inspect.getmembers(obj)
    attr_dict = {}
    for member in members:
        name = member[0]
        value = member[1]
        if name.startswith("__") and name.endswith("__"):
            continue
        if not inspect.isroutine(value):
            attr_dict[name] = value
    return attr_dict


def is_null(obj: object) -> bool:
    """
    Checks if the object is null.
    :param obj: object
    :return: bool type to check if the object is null
    """
    return obj is None


def _compress_bytes(value: bytes) -> bytes:
    """Compresses bytes instance"""
    return zlib.compress(value)


def _decompress_bytes(value: bytes) -> bytes:
    """Decompresses bytes instance"""
    return zlib.decompress(value)
