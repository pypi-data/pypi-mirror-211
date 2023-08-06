"""Includes TransferLearningSettings class"""
from organon.ml.common.enums.optimizer_type import OptimizerType


class TransferLearningSettings:
    """Settings for transfer learning in object classification"""

    def __init__(self, epoch: int = 20, early_stopping: int = 2, optimizer: OptimizerType = OptimizerType.ADAM,
                 dropout: float = 0.2, learning_rate: float = 0.001):
        self.epoch = epoch
        self.early_stopping = early_stopping
        self.optimizer = optimizer
        self.dropout = dropout
        self.learning_rate = learning_rate
