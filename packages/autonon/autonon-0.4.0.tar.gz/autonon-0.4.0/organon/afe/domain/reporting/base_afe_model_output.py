"""
This module includes BaseAfeModelOutput class.
"""
from datetime import datetime
from typing import Dict, List, TypeVar, Generic

from organon.afe.domain.enums.afe_learning_type import AfeLearningType
from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature
from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats
from organon.afe.domain.reporting.runtime_statistics import RuntimeStatistics
from organon.afe.domain.reporting.transformation import Transformation
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.target_descriptor import TargetDescriptor

AfeFeatureType = TypeVar("AfeFeatureType", bound=BaseAfeFeature)


class BaseAfeModelOutput(Generic[AfeFeatureType]):
    """Base AFE output information of model"""

    def __init__(self):
        self.model_identifier: str = None
        self.build_date: datetime = None
        self.output_features: Dict[str, AfeFeatureType] = None
        self.transformations: Dict[str, Transformation] = None
        self.transaction_file_stats: TransactionFileStats = None
        self.runtime_stats: RuntimeStatistics = None
        self.trx_entity_column: str = None
        self.trx_date_columns: Dict[str, AfeDateColumn] = None
        self.target_descriptor: TargetDescriptor = None
        self.final_column_metrics: List[dict] = None
        self.afe_learning_type: AfeLearningType = None
        self.all_features: Dict[str, AfeFeatureType] = None
