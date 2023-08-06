"""Includes DqConstants class."""
from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.fl.security.helpers.encryption_helper import EncryptionHelper


class DqConstants:
    """Stores dq constants"""

    DEFAULT_PERCENTILE_LIST = [0.05, 1, 5, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 95, 99, 99.5]
    NUMERICAL_STATISTICS_MIN_CARDINALITY = 50
    NUMERICAL_STATISTICS_MAX_NUM_OF_INTERVALS = 20
    NUMERICAL_STATISTICS_MIN_INTERVAL_SIZE = 250
    OUTLIER_PARAM_DEFAULT = 3
    CALCULATION_LIMIT_DEFAULT = 5
    MAX_NOMINAL_CARDINALITY_COUNT_DEFAULT = 100
    CONTROL_MAXIMUM_NOM_CARDINALITY_DEFAULT = 1000
    TRAFFIC_LIGHT_THRESHOLD_GREEN = 0.2
    TRAFFIC_LIGHT_THRESHOLD_YELLOW = 0.4
    PSI_THRESHOLD_GREEN = 0.1
    PSI_THRESHOLD_YELLOW = 0.2
    Z_SCORE_DEFAULT = 1.96
    MINIMUM_CARDINALITY_DEFAULT = 1
    MINIMUM_INJECTION = 5
    NOMINAL_COLUMN_TYPES = [ColumnNativeType.String, ColumnNativeType.Date]
    __SECRET_KEY_DEFAULT = "qwertyuıop"  # nosec
    __secret_key: str = __SECRET_KEY_DEFAULT

    @staticmethod
    def get_secret_key():
        """Returns value of secret key"""
        secret_key = DqConstants.__secret_key
        if secret_key == DqConstants.__SECRET_KEY_DEFAULT:
            LogHelper.warning("Secret key not set. Will use default secret key. Set secret key for security.")
        return secret_key

    @staticmethod
    def set_secret_key(secret_key: str):
        """Sets global encryption secret key for AFE"""
        if len(secret_key) > EncryptionHelper.SECRET_KEY_MAX_LENGTH:
            raise KnownException(f"secret_key maximum length is {EncryptionHelper.SECRET_KEY_MAX_LENGTH}")
        DqConstants.__secret_key = secret_key
