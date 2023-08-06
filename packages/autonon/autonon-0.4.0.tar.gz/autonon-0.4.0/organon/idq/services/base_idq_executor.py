"""Includes IDQ class."""
import abc
from typing import Optional, List, TypeVar, Generic, Dict

import organon
from organon.common.helpers import dev_mode_helper
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.idq.core.dq_constants import DqConstants
from organon.idq.domain.businessobjects.dq_calculation_output import DqCalculationOutput
from organon.idq.domain.reporting.objects.base_dq_output_report import BaseDqOutputReport
from organon.idq.domain.services.base_user_input_service import BaseUserInputService
from organon.idq.domain.services.dq_full_process_executor import DqFullProcessExecutor
from organon.idq.domain.settings.abstractions.dq_full_process_input import DqFullProcessInput
from organon.idq.services.idq_application_operations import IdqApplicationOperations
from organon.idq.services.user_settings.base_dq_user_input import BaseDqUserInput

UserInputServiceType = TypeVar("UserInputServiceType", bound=BaseUserInputService)
DqUserInputType = TypeVar("DqUserInputType", bound=BaseDqUserInput)


class BaseIDQ(Generic[UserInputServiceType, DqUserInputType], metaclass=abc.ABCMeta):
    """User service class for IDQ."""

    def __init__(self):
        self._initialize_idq()
        self.results: Optional[BaseDqOutputReport] = None
        self.calculation_outputs: Optional[List[DqCalculationOutput]] = None
        self._user_settings: DqUserInputType = self._get_user_settings_instance()

    @abc.abstractmethod
    def _get_user_settings_instance(self) -> DqUserInputType:
        """Returns empty DqUserInput instance"""

    @classmethod
    def _initialize_idq(cls):
        IdqApplicationOperations.initialize_app()

    def execute(self) -> BaseDqOutputReport:
        """Executes idq and returns results"""
        helper = self._get_user_input_service()
        full_process_input = helper.convert_to_full_process_input()
        executor = self._get_dq_full_process_executor(full_process_input)
        results, calculation_results = executor.execute()
        self.results = results
        self.calculation_outputs = calculation_results
        return results

    @classmethod
    def init_dev_mode(cls, log_to_console: bool = True, log_file: str = "application.log"):
        """Initializes development mode."""
        dev_mode_helper.init_dev_mode(organon.idq.__name__, log_to_console=log_to_console, log_file=log_file)

    @abc.abstractmethod
    def _get_user_input_service(self) -> UserInputServiceType:
        """Returns UserInputService instance"""

    @classmethod
    def _get_dq_full_process_executor(cls, full_process_input: DqFullProcessInput) -> DqFullProcessExecutor:
        return DqFullProcessExecutor(full_process_input)

    def _check_results(self):
        if self.results is None:
            raise ValueError("You should run execute function first to get the results.")

    def set_settings(self,
                     column_benchmark_horizons: Dict[str, int] = None,
                     duplicate_control_columns: List[str] = None,
                     maximum_nom_cardinality: int = DqConstants.CONTROL_MAXIMUM_NOM_CARDINALITY_DEFAULT,
                     minimum_cardinality: int = DqConstants.MINIMUM_CARDINALITY_DEFAULT,
                     traffic_light_threshold_yellow: float = DqConstants.TRAFFIC_LIGHT_THRESHOLD_YELLOW,
                     traffic_light_threshold_green: float = DqConstants.TRAFFIC_LIGHT_THRESHOLD_GREEN,
                     psi_threshold_yellow: float = DqConstants.PSI_THRESHOLD_YELLOW,
                     psi_threshold_green: float = DqConstants.PSI_THRESHOLD_GREEN,
                     z_score: float = DqConstants.Z_SCORE_DEFAULT,
                     excluded_test_groups: List[str] = None,
                     test_group_benchmark_horizons: Dict[str, int] = None,
                     included_column_names: List[str] = None,
                     excluded_column_names: List[str] = None,
                     column_default_values: Dict[str, List[str]] = None,
                     include_date_columns: bool = None
                     ):
        """
        Adds comparison settings

        :param column_benchmark_horizons:
        :param duplicate_control_columns:
        :param minimum_cardinality:
        :param maximum_nom_cardinality:
        :param traffic_light_threshold_yellow:
        :param traffic_light_threshold_green:
        :param psi_threshold_yellow:
        :param psi_threshold_green:
        :param z_score:
        :param excluded_test_groups:
        :param test_group_benchmark_horizons:
        :param included_column_names:
        :param excluded_column_names:
        :param column_default_values:
        :param include_date_columns:
        """
        # todo parametre açıklamaları eklenecek
        # pylint: disable=too-many-arguments
        self._user_settings.set_comparison_params(column_benchmark_horizons, duplicate_control_columns,
                                                  maximum_nom_cardinality, minimum_cardinality,
                                                  traffic_light_threshold_yellow, traffic_light_threshold_green,
                                                  psi_threshold_yellow, psi_threshold_green,
                                                  z_score, excluded_test_groups, test_group_benchmark_horizons,
                                                  included_column_names, excluded_column_names, column_default_values,
                                                  include_date_columns)

    def _check_calculation_results(self):
        if self.calculation_outputs is None:
            raise KnownException("No calculation results generated yet.")

    @staticmethod
    def set_secret_key(secret_key: str):
        """Sets secret key for encryption tasks used during serialization etc."""
        DqConstants.set_secret_key(secret_key)
