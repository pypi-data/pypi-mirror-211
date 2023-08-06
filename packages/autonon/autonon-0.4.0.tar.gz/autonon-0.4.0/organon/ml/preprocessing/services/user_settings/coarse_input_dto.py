"""This module includes Coarse Class input data class."""
from dataclasses import dataclass


@dataclass
class CoarseInputDto:
    """Data class for coarse classing."""
    test_ratio: float
    target_column_type: str
    min_class_size: int
    max_leaf_nodes: int
    stability_check: bool
    stability_threshold: float
    random_state: int
    positive_class: str
    negative_class: str
