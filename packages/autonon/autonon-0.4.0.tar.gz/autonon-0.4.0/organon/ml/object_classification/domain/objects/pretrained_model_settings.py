"""Includes PretrainedModelSettings class"""
from typing import Optional

from organon.ml.common.enums.pretrained_model_type import PretrainedModelType


class PretrainedModelSettings:
    """Settings related to pretrained model in object classification"""

    def __init__(self, model: PretrainedModelType = PretrainedModelType.XCEPTION, weights: Optional[str] = "imagenet"):
        self.model = model
        self.weights = weights
