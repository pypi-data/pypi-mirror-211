"""Includes UserInputService class."""
from typing import List, Dict

import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType
from organon.idq.domain.services.base_user_input_service import BaseUserInputService
from organon.idq.domain.services.user_input_validation_service import UserInputValidationService
from organon.idq.services.user_settings.dq_user_input import DqUserInput


class UserInputService(BaseUserInputService[DqUserInput]):
    """Includes methods to read and validate dq user input"""

    def __init__(self, user_input: DqUserInput):
        super().__init__(user_input)

    def _get_input_validation_service(self, source_columns: List[Dict[str, ColumnNativeType]]) \
            -> UserInputValidationService:
        return UserInputValidationService(self._user_input, source_columns[0])

    def _get_columns_in_sources(self) -> List[Dict[str, ColumnNativeType]]:
        self._validate_input_source_settings(self._user_input.calc_params.input_source_settings)
        return [self._get_column_native_types(self._user_input.calc_params.input_source_settings)]

    def _get_source_type(self):
        comp_source = self._user_input.calc_params.input_source_settings.source
        if isinstance(comp_source, str):
            return DqRecordSourceType.TEXT
        if isinstance(comp_source, pd.DataFrame):
            return DqRecordSourceType.DATA_FRAME
        raise ValueError("Invalid input source type!")

    def _get_calc_params(self, source_columns: List[Dict[str, ColumnNativeType]]):
        return self._get_calculation_params_from_user_multi_part_calc_params(self._user_input.calc_params,
                                                                             list(source_columns[0].keys()))
