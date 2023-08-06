"""Includes UserInputValidationService class."""
from typing import Dict

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.idq.domain.services.base_user_input_validation_service import BaseUserInputValidationService
from organon.idq.services.user_settings.dq_user_input import DqUserInput


class UserInputValidationService(BaseUserInputValidationService[DqUserInput]):
    """Service for validating settings in DqUserInput"""

    def __init__(self, user_input: DqUserInput, column_native_types: Dict[str, ColumnNativeType]):
        super().__init__(user_input)
        self.column_native_types = column_native_types

    def validate(self):
        """Executes validation"""
        if self.user_input.calc_params is None:
            raise KnownException("Calculation settings not given")

        super().validate()

        self._validate_calculation_parameters(0, self.user_input.calc_params, self.column_native_types)
        self._validate_included_excluded_columns([list(self.column_native_types.keys())])
        self._validate_comparison_column_info(list(self.column_native_types.keys()))
        self._validate_column_metadata_list(list(self.column_native_types.keys()))
