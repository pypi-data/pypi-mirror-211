"""
This module includes TargetFileRecord class.
"""
import numpy as np

from organon.afe.domain.enums.binary_target_class import BinaryTargetClass


class TargetFileRecord:
    """
    Class corresponding to a row in target file
    """

    def __init__(self):
        self.entity_id: str = None
        self.event_date: int = None
        self.target_scalar: np.float64 = None
        self.target_binary: BinaryTargetClass = None
        self.target_multi_class: np.object_ = None
