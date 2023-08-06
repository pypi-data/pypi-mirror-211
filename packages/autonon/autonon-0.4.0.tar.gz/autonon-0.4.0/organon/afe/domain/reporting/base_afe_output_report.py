"""
This module includes BaseAfeOutputReport class.
"""
from datetime import datetime
from typing import Dict, List, Generic, TypeVar

from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature
from organon.afe.domain.reporting.transformation import Transformation


class FeatureCountReport:
    """Stores feature count statistics grouped by different fields"""

    def __init__(self, by_dimension: Dict[str, int], by_quantity: Dict[str, int], by_operator: Dict[str, int],
                 by_time_window: Dict[str, int]):
        self.by_dimension = by_dimension
        self.by_quantity = by_quantity
        self.by_operator = by_operator
        self.by_time_window = by_time_window


AfeFeatureType = TypeVar("AfeFeatureType", bound=BaseAfeFeature)


class BaseAfeOutputReport(Generic[AfeFeatureType]):
    """Afe output information to be reported."""

    def __init__(self):
        self.model_identifier: str = None
        self.output_features: Dict[str, AfeFeatureType] = None
        self.all_features: Dict[str, AfeFeatureType] = None
        self.dimension_names_map: Dict[str, Dict[int, str]] = None
        self.transformations: Dict[str, Transformation] = None
        self.execution_time: float = None
        self.memory_usage: Dict[datetime, float] = None
        self.cpu_usage: Dict[datetime, float] = None
        self.event_times: Dict[str, datetime] = None
        self.feature_counts_report: FeatureCountReport = None
        self.final_column_metrics: List[dict] = None
