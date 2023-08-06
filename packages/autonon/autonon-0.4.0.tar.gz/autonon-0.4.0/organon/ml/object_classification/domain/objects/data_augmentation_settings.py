"""Includes DataAugmentationSettings class."""
from organon.ml.common.enums.random_flip_type import RandomFlipType


class DataAugmentationSettings:
    """Settings for fine tuning in object classification"""

    def __init__(self, random_flip: RandomFlipType = RandomFlipType.HORIZONTAL_AND_VERTICAL,
                 random_rotation: float = 0.1, random_zoom: float = 0.1):
        self.random_flip: RandomFlipType = random_flip
        self.random_rotation: float = random_rotation
        self.random_zoom: float = random_zoom
