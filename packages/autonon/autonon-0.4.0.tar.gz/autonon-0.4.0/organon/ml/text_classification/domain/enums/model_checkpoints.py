"""Includes ModelCheckpoints enum class"""
from enum import Enum, auto


class ModelCheckpoints(Enum):
    """Pretrained model types"""

    ROBERTA_BASE = auto()
    DISTILBERT_BASE = auto()
    BERT_BASE = auto()
    BERT_BASE_TR_128 = auto()
    BERT_BASE_MLINGUAL = auto()
    BERT_BASE_TR_SENTIMENT = auto()
