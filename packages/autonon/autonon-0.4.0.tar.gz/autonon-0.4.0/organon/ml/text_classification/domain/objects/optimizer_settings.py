"""Includes TransferLearningSettings class"""


class OptimizerSettings:
    """Settings for transfer learning in text classification"""

    def __init__(self, learning_rate: float = 1e-5, early_stopping: int = 5, steps_per_epoch: int = None,
                 early_stopping_min_delta: float = 1e-3):
        self.learning_rate: float = learning_rate
        self.early_stopping: int = early_stopping
        self.steps_per_epoch: int = steps_per_epoch
        self.early_stopping_min_delta: float = early_stopping_min_delta
