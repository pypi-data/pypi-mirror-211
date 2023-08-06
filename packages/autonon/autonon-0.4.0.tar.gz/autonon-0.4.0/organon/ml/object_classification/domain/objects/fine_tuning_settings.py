"""Includes FineTuningSettings class."""

from organon.ml.common.enums.optimizer_type import OptimizerType


class FineTuningSettings:
    """Settings for fine tuning in object classification"""

    def __init__(self, epoch: int = 10, early_stopping_patience: int = 2, early_stopping_min_delta: float = 0.001,
                 learning_rate: float = 1e-5, optimizer: OptimizerType = OptimizerType.ADAM):
        self.epoch = epoch
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_min_delta = early_stopping_min_delta
        self.learning_rate = learning_rate
        self.optimizer = optimizer
