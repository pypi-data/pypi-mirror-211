"""Includes UserInputValidationService class."""
from typing import List, Dict, Generic, TypeVar, Union

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import list_helper
from organon.fl.core.helpers.string_helper import is_null_or_empty
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.idq.core.dq_constants import DqConstants
from organon.idq.services.user_settings.base_dq_user_input import BaseDqUserInput
from organon.idq.services.user_settings.user_calculation_params import UserCalculationParams
from organon.idq.services.user_settings.user_input_source_settings import UserInputSourceSettings
from organon.idq.services.user_settings.user_multi_partition_calculation_params import \
    UserMultiPartitionCalcParams

DqUserInputType = TypeVar("DqUserInputType", bound=BaseDqUserInput)


class BaseUserInputValidationService(Generic[DqUserInputType]):
    """Service for validating settings in DqUserInput"""

    def __init__(self, user_input: DqUserInputType):
        self.user_input: DqUserInputType = user_input

    def validate(self):
        """Executes validation and returns columns and their native types in test input source"""
        self._validate_common_comparison_params()

    def _validate_common_comparison_params(self):
        self._check_range(self.user_input.minimum_cardinality, 0, 100, "Minimum cardinality")
        self._check_range(self.user_input.traffic_light_threshold_green, 0, 0.2, "Traffic Light Threshold Green")
        self._check_range(self.user_input.traffic_light_threshold_yellow, 0.2, 0.4, "Traffic Light Threshold Yellow")
        self._check_range(self.user_input.psi_threshold_green, 0, 0.1, "Psi Threshold Green")
        self._check_range(self.user_input.psi_threshold_yellow, 0.1, 0.2, "Psi Threshold Yellow")
        self._check_range(self.user_input.z_score, 0, 5, "Z Score")
        self._validate_test_groups_info()

    def _validate_included_excluded_columns(self, source_columns: List[List[str]]):
        included_cols = self.user_input.included_column_names
        excluded_cols = self.user_input.excluded_column_names
        included_cols = included_cols if included_cols is not None else []
        excluded_cols = excluded_cols if excluded_cols is not None else []
        common_cols = [col for col in included_cols if col in excluded_cols]
        if len(common_cols) > 0:
            raise KnownException(f"Columns {common_cols} are given in both "
                                 f"included_column_names and excluded_columns_names")
        for included_col in included_cols:
            for columns in source_columns:
                if included_col not in columns:
                    raise KnownException(f"Column '{included_col}' (in included_column_names) does not exist "
                                         f"in all data sources")

    def _validate_comparison_column_info(self, source_column_names: List[str]):
        if self.user_input.column_benchmark_horizons is not None:
            non_existing_comp_col_names = [col for col in self.user_input.column_benchmark_horizons
                                           if col not in source_column_names]
            if len(non_existing_comp_col_names) > 0:
                raise KnownException(f"Following comparison columns(given in column_benchmark_horizons) do not exist"
                                     f" in test calculation input source: {non_existing_comp_col_names}")
            num_calcs = self._get_number_of_calculations()
            for col, horizon in self.user_input.column_benchmark_horizons.items():
                if horizon > num_calcs - 1:
                    LogHelper.warning(f"There are {num_calcs - 1} control calculations but benchmark horizon is "
                                      f"given {horizon} for column '{col}'")

        if self.user_input.duplicate_control_columns is not None:
            non_existing_comp_col_names = [col for col in self.user_input.duplicate_control_columns
                                           if col not in source_column_names]
            if len(non_existing_comp_col_names) > 0:
                raise KnownException(f"Following comparison columns(given in duplicate_control_columns) do not exist "
                                     f"in test calculation input source: {non_existing_comp_col_names}")

    def _get_eligible_column_types(self):
        col_types = [ColumnNativeType.Numeric] + DqConstants.NOMINAL_COLUMN_TYPES
        if self.user_input.include_date_columns is False and ColumnNativeType.Date in col_types:
            col_types.remove(ColumnNativeType.Date)
        return col_types

    def _validate_test_groups_info(self):
        if self.user_input.test_group_benchmark_horizons is not None:
            num_calcs = self._get_number_of_calculations()
            for test_group, horizon in self.user_input.test_group_benchmark_horizons.items():
                if horizon > num_calcs - 1:
                    LogHelper.warning(f"There are {num_calcs - 1} control calculations but benchmark horizon is "
                                      f"given {horizon} for test group '{test_group}'")

    def _get_number_of_calculations(self) -> int:
        calc_params = self.user_input.calc_params
        if list_helper.is_null_or_empty(calc_params.partitions):
            return 1
        return len(calc_params.partitions)

    def _validate_column_metadata_list(self, source_column_names: List[str]):
        if self.user_input.column_default_values is not None:
            non_existing_comp_col_names = [col for col in self.user_input.column_default_values
                                           if col not in source_column_names]
            if len(non_existing_comp_col_names) > 0:
                raise KnownException(f"Following columns(given in column_default_values) do not exist in "
                                     f"test calculation input source: {non_existing_comp_col_names}")

        if self.user_input.excluded_column_names is not None:
            non_existing_comp_col_names = [col for col in self.user_input.excluded_column_names
                                           if col not in source_column_names]
            if len(non_existing_comp_col_names) > 0:
                raise KnownException(f"Following columns(given in excluded_column_names) do not exist in "
                                     f"test calculation input source: {non_existing_comp_col_names}")

    def _validate_calculation_parameters(self, _index: int,
                                         calculation_parameters: Union[UserMultiPartitionCalcParams,
                                                                       UserCalculationParams],
                                         column_native_types: Dict[str, ColumnNativeType]):
        self.validate_calculation_input_source_settings(calculation_parameters.input_source_settings)
        allowed_native_types = self._get_eligible_column_types()
        eligible_column_list = [col for col, native_type in column_native_types.items()
                                if native_type in allowed_native_types]
        if list_helper.is_null_or_empty(eligible_column_list):
            if _index is not None:
                raise KnownException(f"No eligible columns found in data source of Calculation-{_index + 1}")
            raise KnownException("No eligible columns found in data source")

        self._check_range(calculation_parameters.max_nominal_cardinality_count, 0, 100000,
                          "Max. nominal cardinality count")

        if calculation_parameters.outlier_parameter is not None and \
                calculation_parameters.outlier_parameter not in [1.5, 3.0]:
            raise KnownException("Outlier parameter must be either 1.5 or 3")

    @classmethod
    def validate_calculation_input_source_settings(cls, settings: UserInputSourceSettings):
        """Validates input source settings in calculation parameters"""
        if settings.source is None:
            raise KnownException("Input source cannot be None")
        if isinstance(settings.source, str):
            if is_null_or_empty(settings.source.strip()):
                raise KnownException("Input file name is empty")

        cls._check_range(settings.sampling_ratio, 0, 1.0, "Sampling ratio")

    @classmethod
    def _check_range(cls, value: float, min_val: float, max_val: float, definition: str):
        if value is not None and (value < min_val or value > max_val):
            raise KnownException(f"{definition} should be between {min_val} and {max_val}")
