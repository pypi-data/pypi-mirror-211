"""Includes Dq user input classes."""
from typing import List

from organon.idq.services.user_settings.base_dq_user_input import BaseDqUserInput
from organon.idq.services.user_settings.user_multi_partition_calculation_params import UserMultiPartitionCalcParams


class DqUserInput(BaseDqUserInput):
    """User class for all dq settings"""

    def __init__(self):
        super().__init__()
        self.calc_params: UserMultiPartitionCalcParams = None

    def set_multi_partition_calculation(self,
                                        input_source_settings: dict,
                                        max_nominal_cardinality_count: int = None,
                                        outlier_parameter: float = None,
                                        use_population_nominal_stats: bool = None,
                                        name: str = None,
                                        partitions: List[List[dict]] = None):
        """
        Adds calculation settings
        """
        self._check_simple_types(locals(), {
            "input_source_settings": dict,
            "max_nominal_cardinality_count": int,
            "outlier_parameter": (float, int),
            "name": str,
            "partitions": list
        })  # bu satır method'ta en üst satır olmalı (locals kullanımından dolayı)
        self.calc_params = self._get_multi_partition_calculation_params(name, input_source_settings,
                                                                        max_nominal_cardinality_count,
                                                                        outlier_parameter,
                                                                        use_population_nominal_stats,
                                                                        partitions=partitions)
