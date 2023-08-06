"""Includes BlasServiceType enum."""
from enum import Enum, auto


class BlasServiceType(Enum):
    """Blas service types"""
    MKL_BLAS = auto()
    SCIPY_BLAS = auto()
