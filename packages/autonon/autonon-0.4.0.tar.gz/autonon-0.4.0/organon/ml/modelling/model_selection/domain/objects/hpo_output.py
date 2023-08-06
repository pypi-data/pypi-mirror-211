"""Includes HPOOutput class."""
from typing import Dict, Any

import pandas as pd

from organon.ml.modelling.algorithms.core.abstractions.base_modeller import BaseModeller


class HPOOutput:
    """Output of HPOService"""

    def __init__(self):
        self.best_modeller: BaseModeller = None
        self.best_params: Dict[str, Any] = None
        self.summary: pd.DataFrame = None
