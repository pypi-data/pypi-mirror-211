"""Module for SweptAttribute"""
from dataclasses import dataclass
import numpy as np


@dataclass
class SweptAttribute:
    """Info for swept attribute"""
    attribute_index: int = None
    unswept_row: np.ndarray = None
    unswept_col: np.ndarray = None
    swept_row: np.ndarray = None
    swept_col: np.ndarray = None
