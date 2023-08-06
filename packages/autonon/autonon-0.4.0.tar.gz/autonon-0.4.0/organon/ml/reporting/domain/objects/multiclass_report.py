"""Includes MulticlassReport class."""
from typing import Dict, Tuple

import pandas as pd

from organon.ml.reporting.domain.objects.base_report import BaseReport


class MulticlassReport(BaseReport):
    """Report for multiclass classification"""

    def __init__(self):
        self.scores: pd.DataFrame = None
        self.confusion_matrices: Dict[Tuple, pd.DataFrame] = None
        self.classification_reports: Dict[Tuple, pd.DataFrame] = None
