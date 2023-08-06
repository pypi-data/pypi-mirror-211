"""Includes MultiClassReporterSettings class."""
from dataclasses import dataclass
from typing import List

import numpy as np

from organon.ml.reporting.settings.objects.reporter_settings import ReporterSettings


@dataclass
class MultiClassReporterSettings(ReporterSettings):
    """Settings for MultiClass Reporter service"""
    probability_values: np.array = None
    ordered_class_names: List = None
