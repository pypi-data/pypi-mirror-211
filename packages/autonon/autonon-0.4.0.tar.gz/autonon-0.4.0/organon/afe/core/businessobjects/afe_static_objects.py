"""
This module includes AfeStaticObjects class.
"""
from datetime import datetime

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.fl.security.helpers.encryption_helper import EncryptionHelper


class AfeStaticObjects:
    """
    This class has static attributes corresponding to AFE constants.
    """
    distinct_entities_table_name_prefix: str = None
    distinct_entities_entity_column_name: str = None
    event_date_column_name: str = None
    empty_date_col_prefix: str = None
    no_date_col_default_date: datetime = None

    empty_quantity_column: str = None
    empty_dimension_column: str = None
    empty_dimension_val: str = None
    empty_dimension_index: int = None

    log_for_debugging: bool = None
    enable_trace_logging: bool = None
    __SECRET_KEY_DEFAULT = "qwertyuıop"  # nosec
    __secret_key: str = __SECRET_KEY_DEFAULT

    @staticmethod
    def set_defaults():
        """Sets default values."""
        AfeStaticObjects.distinct_entities_table_name_prefix = "DET"
        AfeStaticObjects.distinct_entities_entity_column_name = "ENTITY_ID"
        AfeStaticObjects.event_date_column_name = "EVENT_DATE"
        AfeStaticObjects.empty_date_col_prefix = "__DATE"
        AfeStaticObjects.no_date_col_default_date = datetime(1971, 1, 1)

        AfeStaticObjects.empty_quantity_column = "NoQuantity"
        AfeStaticObjects.empty_dimension_column = "NoDimension"
        AfeStaticObjects.empty_dimension_val = "NULL"
        AfeStaticObjects.empty_dimension_index = 0

        AfeStaticObjects.log_for_debugging = False

    @staticmethod
    def get_secret_key():
        """Returns value of secret key"""
        secret_key = AfeStaticObjects.__secret_key
        if secret_key == AfeStaticObjects.__SECRET_KEY_DEFAULT:
            LogHelper.warning("Secret key not set. Will use default secret key. Set secret key for security.")
        return secret_key

    @staticmethod
    def set_secret_key(secret_key: str):
        """Sets global encryption secret key for AFE"""
        if len(secret_key) > EncryptionHelper.SECRET_KEY_MAX_LENGTH:
            raise KnownException(f"secret_key maximum length is {EncryptionHelper.SECRET_KEY_MAX_LENGTH}")
        AfeStaticObjects.__secret_key = secret_key
