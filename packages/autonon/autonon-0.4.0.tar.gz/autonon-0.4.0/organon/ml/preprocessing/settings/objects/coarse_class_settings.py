"""Includes CoarseClassSettings class."""
from dataclasses import dataclass

from organon.ml.common.enums.target_type import TargetType


@dataclass
class CoarseClassSettings:
    """Settings for CoarseClass service"""
    test_ratio: float
    min_class_size: int
    target_type: TargetType
    max_leaf_nodes: int
    stability_check: bool
    stability_threshold: float
    random_state: int
    positive_class: str
    negative_class: str
