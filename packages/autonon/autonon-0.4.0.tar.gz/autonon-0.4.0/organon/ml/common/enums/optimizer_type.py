"""Includes OptimizerType enum class"""
from enum import Enum, auto


class OptimizerType(Enum):
    """Optimizer types"""
    ADAM = auto()
    ADADELTA = auto()
    ADAGRAD = auto()
    NADAM = auto()
    FTRL = auto()
    ADAMAX = auto()
    SGD = auto()
    RMSPROP = auto()
    