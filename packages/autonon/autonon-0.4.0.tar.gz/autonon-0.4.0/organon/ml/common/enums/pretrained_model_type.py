"""Includes PretrainedModelType enum class"""
from enum import Enum, auto


class PretrainedModelType(Enum):
    """Pretrained model types"""
    XCEPTION = auto()
    RES_NET_50_V2 = auto()
    EFFICIENT_NET_B4 = auto()
    EFFICIENT_NET_B7 = auto()
    INCEPTION_RES_NET_V2 = auto()
