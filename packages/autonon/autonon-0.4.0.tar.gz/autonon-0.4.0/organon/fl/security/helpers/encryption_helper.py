"""
this module includes encryption helper functions.
"""
import base64
import os
import string
from random import SystemRandom
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from organon.fl.core.exceptionhandling.known_exception import KnownException


class EncryptionHelper:
    """Holds static methods for encryption/decryption"""

    GCM_IV_LENGTH = 12
    SECRET_KEY_MAX_LENGTH = 16

    @staticmethod
    def generate_key():
        """Generates random key of length 16"""
        all_chars = string.ascii_letters + string.digits + string.punctuation
        return "".join(SystemRandom().sample(all_chars, EncryptionHelper.SECRET_KEY_MAX_LENGTH))

    @staticmethod
    def encrypt_string(value: str, secret_key: str = None) -> str:
        """
        Returns encrypted version of given string
        :param value: string to be encrypted
        :param secret_key: secret key to be used in encryption
        :type value: str
        :return: Encrypted version of string on base64
        """
        byte_val = bytes(value, encoding="utf-8")
        b64_str = base64.b64encode(EncryptionHelper.encrypt_bytes(byte_val, secret_key=secret_key)[0]).decode()
        return b64_str

    @staticmethod
    def decrypt_string(encrypted_str: str, secret_key: str) -> str:
        """
        Decrypts given string
        :param encrypted_str: string to be decrypted
        :param secret_key: secret key to be used in encryption
        :type encrypted_str: str
        :return: Decrypted version of string
        """
        data_bin = base64.b64decode(encrypted_str)
        output = EncryptionHelper.decrypt_bytes(data_bin, secret_key)
        return output.decode(encoding="utf-8")

    @staticmethod
    def __get_normalized_key(key: str) -> bytes:
        max_len = EncryptionHelper.SECRET_KEY_MAX_LENGTH
        lst = bytearray(key, "utf-8")
        key_len = len(lst)
        if key_len > max_len:
            raise KnownException(f"Secret key max length is: {max_len}")
        out = lst.copy()
        out[key_len:] = [0 for _ in range(max_len - key_len)]
        return bytes(out)

    @staticmethod
    def encrypt_bytes(byte_val: bytes, secret_key: str = None) -> Tuple[bytes, str]:
        """
        Encrypts given bytes value.
        :param byte_val: bytes to be encrypted
        :param secret_key: secret key to be used in encryption
        :return: encrypted version of byte_val
        """
        if secret_key is None:
            secret_key = EncryptionHelper.generate_key()
        init_vector = os.urandom(EncryptionHelper.GCM_IV_LENGTH)
        key = EncryptionHelper.__get_normalized_key(secret_key)

        aesgcm = AESGCM(key)
        encrypted = aesgcm.encrypt(init_vector, byte_val, None)

        return init_vector + encrypted, secret_key

    @staticmethod
    def decrypt_bytes(encrypted_bytes: bytes, secret_key: str) -> bytes:
        """
        Decrypts given bytes value
        :param encrypted_bytes: bytes to be decrypted
        :param secret_key: secret key used in encryption
        :return: Decrypted version of encrypted_bytes
        """
        if secret_key is None:
            raise KnownException("Cannot decrypt. Secret_key is None.")
        iv_bytes = encrypted_bytes[:EncryptionHelper.GCM_IV_LENGTH]
        encrypted_data = encrypted_bytes[EncryptionHelper.GCM_IV_LENGTH:]
        key = EncryptionHelper.__get_normalized_key(secret_key)
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(iv_bytes, encrypted_data, None)
