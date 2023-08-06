"""Includes UserCalculationParams class."""
from typing import List

from organon.idq.services.user_settings.base_user_calculation_params import BaseUserCalculationParams
from organon.idq.services.user_settings.user_partition_info import UserPartitionInfo


class UserMultiPartitionCalcParams(BaseUserCalculationParams):
    """Calculation settings user class"""

    def __init__(self, calc_name, input_source_settings, max_nom_card_count, outlier_param, use_pop_nom_stats,
                 partitions=None):
        super().__init__(calc_name, input_source_settings, max_nom_card_count, outlier_param, use_pop_nom_stats)
        self.partitions: List[List[UserPartitionInfo]] = partitions
