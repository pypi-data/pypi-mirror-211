"""Includes IDQ class."""
from typing import List

from organon.idq.core.dq_constants import DqConstants
from organon.idq.domain.services.user_input_service import UserInputService
from organon.idq.services.base_idq_executor import BaseIDQ
from organon.idq.services.user_settings.dq_user_input import DqUserInput


class IDQ(BaseIDQ[UserInputService, DqUserInput]):
    """User service class for IDQ."""

    def _get_user_settings_instance(self) -> DqUserInput:
        return DqUserInput()

    def _get_user_input_service(self) -> UserInputService:
        return UserInputService(self._user_settings)

    def set_calculation_settings(self,
                                 input_source_settings: dict,
                                 max_nominal_cardinality_count: int = DqConstants.MAX_NOMINAL_CARDINALITY_COUNT_DEFAULT,
                                 outlier_parameter: float = DqConstants.OUTLIER_PARAM_DEFAULT,
                                 name: str = None,
                                 partitions: List[List[dict]] = None):
        """
        Sets calculation settings

        :param input_source_settings:
        :param max_nominal_cardinality_count:
        :param outlier_parameter:
        :param name:
        :param partitions:
        """
        # todo parametre açıklamaları eklenecek
        # pylint: disable=too-many-arguments
        self._user_settings.set_multi_partition_calculation(input_source_settings, max_nominal_cardinality_count,
                                                            outlier_parameter, None,
                                                            name, partitions=partitions)
