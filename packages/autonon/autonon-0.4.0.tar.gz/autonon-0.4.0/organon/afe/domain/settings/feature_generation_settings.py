"""This module includes AfeDateColumnSettings class."""
from datetime import datetime
from typing import List

from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.temporal_grid import TemporalGrid
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.common.reader_helper import get_values_from_kwargs


class FeatureGenerationSettings:
    """AFE settings per date column in transaction data"""

    ATTR_DICT = {
        "date_column": AfeDateColumn,
        "dimension_columns": List[str],
        "quantity_columns": List[str],
        "temporal_grids": List[TemporalGrid],
        "date_resolution": DateResolution,
        "horizon_list": List[int],
        "included_operators": List[AfeOperator],
        "date_offset": int,
        "max_observation_date": datetime
    }

    def __init__(self, **kwargs):
        self.date_column: AfeDateColumn = None
        self.dimension_columns: List[str] = None
        self.quantity_columns: List[str] = None
        self.temporal_grids: List[TemporalGrid] = None
        self.date_resolution: DateResolution = None
        self.horizon_list: List[int] = None
        self.included_operators: List[AfeOperator] = None
        self.date_offset: int = None
        self.max_observation_date: datetime = None

        get_values_from_kwargs(self, self.ATTR_DICT, kwargs)
