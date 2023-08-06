"""Includes ReporterSettings class."""
from dataclasses import dataclass

import pandas as pd

from organon.ml.common.enums.target_type import TargetType


@dataclass
class ReporterSettings:
    """Settings for Reporter services"""
    data: pd.DataFrame
    target_column: str
    score_column: str
    target_type: TargetType
    id_str_column: str
    split_column: str
    num_bins: int
