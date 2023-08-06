"""
THis module keeps the OsTypeId enum class.
"""
from enum import Enum


class OsType(Enum):
    """
    This class keeps the operating system types.
    """
    NOT_AVAILABLE = 0
    WINDOWS = 1
    LINUX = 2
