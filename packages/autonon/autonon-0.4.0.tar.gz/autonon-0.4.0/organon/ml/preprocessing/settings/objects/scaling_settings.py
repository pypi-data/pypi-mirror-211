"""Includes ScalingSettings class."""
from dataclasses import dataclass

from organon.ml.preprocessing.settings.enums.scaler_type import ScalerType


@dataclass
class ScalingSettings:
    """Settings for ScalingService."""
    strategy: ScalerType
