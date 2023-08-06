"""Includes DataSourceSettings class."""
from typing import Tuple

from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.common.enums.color_type import ColorType


class DataSourceSettings:
    """Settings for fine tuning in object classification"""

    def __init__(self, clf_type: ClassificationType, validation_data_ratio: float = 0.2,
                 image_size: Tuple[int, int] = (150, 150),
                 batch_size: int = 50, color_mode: ColorType = ColorType.RGB, random_seed: int = 42):
        self.clf_type = clf_type
        self.validation_data_ratio = validation_data_ratio
        self.image_size = image_size
        self.batch_size = batch_size
        self.color_mode = color_mode
        self.random_seed = random_seed
