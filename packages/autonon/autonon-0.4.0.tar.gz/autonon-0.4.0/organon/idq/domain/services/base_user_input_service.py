"""Includes UserInputService class."""
import abc
import sys
from typing import Union, List, Optional, Dict, TypeVar, Generic

import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers import list_helper
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.core.helpers.string_helper import is_null_or_empty
from organon.idq.core.dq_constants import DqConstants
from organon.idq.domain.businessobjects.dq_test_group import DqTestGroup
from organon.idq.domain.businessobjects.record_sources.dq_df_record_source import DqDfRecordSource
from organon.idq.domain.businessobjects.record_sources.dq_file_record_source import DqFileRecordSource
from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType
from organon.idq.domain.enums.dq_test_group_type import DqTestGroupType
from organon.idq.domain.services.base_user_input_validation_service import BaseUserInputValidationService
from organon.idq.domain.services.user_input_validation_service import UserInputValidationService
from organon.idq.domain.settings.abstractions.dq_base_calculation_parameters import DqBaseCalculationParameters
from organon.idq.domain.settings.abstractions.dq_full_process_input import DqFullProcessInput
from organon.idq.domain.settings.calculation.dq_df_calculation_parameters import DqDfCalculationParameters
from organon.idq.domain.settings.calculation.dq_file_calculation_parameters import DqFileCalculationParameters
from organon.idq.domain.settings.comparison.dq_df_comparison_parameters import DqDfComparisonParameters
from organon.idq.domain.settings.comparison.dq_file_comparison_parameters import DqFileComparisonParameters
from organon.idq.domain.settings.date_value_definition import DateValueDefinition
from organon.idq.domain.settings.dq_column_metadata import DqColumnMetadata
from organon.idq.domain.settings.dq_comparison_column_info import DqComparisonColumnInfo
from organon.idq.domain.settings.full_process.dq_df_full_process_input import DqDfFullProcessInput
from organon.idq.domain.settings.full_process.dq_file_full_process_input import DqFileFullProcessInput
from organon.idq.domain.settings.input_source.dq_df_input_source_settings import DqDfInputSourceSettings
from organon.idq.domain.settings.input_source.dq_file_input_source_settings import DqFileInputSourceSettings
from organon.idq.domain.settings.partition_info import PartitionInfo
from organon.idq.services.user_settings.base_dq_user_input import BaseDqUserInput
from organon.idq.services.user_settings.user_date_value_definition import UserDateValueDefinition
from organon.idq.services.user_settings.user_input_source_settings import UserInputSourceSettings
from organon.idq.services.user_settings.user_multi_partition_calculation_params import \
    UserMultiPartitionCalcParams
from organon.idq.services.user_settings.user_partition_info import UserPartitionInfo


def _get_or_default(val, default_val):
    if val is None:
        return default_val
    return val


DqUserInputType = TypeVar("DqUserInputType", bound=BaseDqUserInput)

UserInputValidationServiceType = TypeVar("UserInputValidationServiceType", bound=BaseUserInputValidationService)


class BaseUserInputService(Generic[DqUserInputType], metaclass=abc.ABCMeta):
    """Includes methods to read and validate dq user input"""

    def __init__(self, user_input: DqUserInputType):
        self._user_input = user_input
        self._source_type = self._get_source_type()

    def _validate_user_input(self, source_columns: List[Dict[str, ColumnNativeType]]) -> Dict[str, int]:
        """Validates dq user input and returns columns and their native types in test calculation."""
        service = self._get_input_validation_service(source_columns)
        return service.validate()

    def convert_to_full_process_input(self) -> DqFullProcessInput:
        """Generates DqFullProcessInput from DqUserInput"""
        source_columns = self._get_columns_in_sources()
        self._validate_user_input(source_columns)
        full_proc_inp = self._get_full_proc_input_instance()
        full_proc_inp.calculation_parameters = self._get_calc_params(source_columns)
        full_proc_inp.comparison_parameters = self.__get_comp_params(len(full_proc_inp.calculation_parameters))
        full_proc_inp.use_supplied_calcs_as_comp_inputs = self._user_input.use_supplied_calcs_as_comp_inputs

        return full_proc_inp

    @classmethod
    def _validate_input_source_settings(cls, settings: UserInputSourceSettings):
        UserInputValidationService.validate_calculation_input_source_settings(settings)

    @abc.abstractmethod
    def _get_columns_in_sources(self) -> List[Dict[str, ColumnNativeType]]:
        pass

    def _get_column_native_types(self, settings: UserInputSourceSettings) -> Dict[str, ColumnNativeType]:
        # this method should be called after input source settings validation
        if isinstance(settings.source, str):
            return self.__get_column_native_types_for_file(settings)
        if isinstance(settings.source, pd.DataFrame):
            return self.__get_column_native_types_for_df(settings.source)
        raise ValueError

    @classmethod
    def __get_column_native_types_for_file(cls, settings: UserInputSourceSettings):
        sep = settings.csv_separator if settings.csv_separator is not None else ","
        data_frame = pd.read_csv(settings.source, sep=sep, nrows=100)
        data_frame = data_frame.convert_dtypes()
        return cls.__get_column_native_types_for_df(data_frame)

    @classmethod
    def __get_column_native_types_for_df(cls, data_frame: pd.DataFrame):
        return {col: get_column_native_type(data_frame, col) for col in data_frame.columns}

    @abc.abstractmethod
    def _get_input_validation_service(self, source_columns: List[Dict[str, ColumnNativeType]]) \
            -> UserInputValidationServiceType:
        """Returns service for user input validation"""

    @abc.abstractmethod
    def _get_calc_params(self, source_columns: List[Dict[str, ColumnNativeType]]):
        """Generates and returns list of calculation parameters"""

    def _get_calculation_params_from_user_multi_part_calc_params(self,
                                                                 user_calc_param: UserMultiPartitionCalcParams,
                                                                 all_columns: List[str]) \
            -> List[DqBaseCalculationParameters]:

        partitions = user_calc_param.partitions if user_calc_param.partitions is not None else [None]

        all_calc_params = []
        for i, partition_info in enumerate(partitions):
            calc_param = self._get_calc_param_instance()
            included_columns = self._decide_included_columns(all_columns)
            calc_param.input_source_settings = self._get_input_source_settings(i,
                                                                               user_calc_param.input_source_settings,
                                                                               partition_info,
                                                                               included_columns)
            calc_param.calculation_name = self.__get_calculation_name(
                calc_param.input_source_settings.partition_info_list)

            calc_param.outlier_parameter = _get_or_default(user_calc_param.outlier_parameter,
                                                           DqConstants.OUTLIER_PARAM_DEFAULT)
            calc_param.max_nominal_cardinality_count = \
                _get_or_default(user_calc_param.max_nominal_cardinality_count,
                                DqConstants.MAX_NOMINAL_CARDINALITY_COUNT_DEFAULT)
            calc_param.use_population_nominal_stats = user_calc_param.use_population_nominal_stats
            calc_param.column_dq_metadata_list = self._get_col_metadata_list(
                self._user_input.excluded_column_names,
                self._user_input.column_default_values)
            calc_param.nominal_column_types = DqConstants.NOMINAL_COLUMN_TYPES.copy()
            if self._user_input.include_date_columns is False and \
                    ColumnNativeType.Date in calc_param.nominal_column_types:
                calc_param.nominal_column_types.remove(ColumnNativeType.Date)
            all_calc_params.append(calc_param)

        return all_calc_params

    def _decide_included_columns(self, all_columns: List[str]):
        excluded_columns = self._user_input.excluded_column_names
        if excluded_columns is not None:
            return [col for col in all_columns if col not in excluded_columns]
        return self._user_input.included_column_names

    @staticmethod
    def __get_calculation_name(partition_info_list: List[PartitionInfo]):
        calculation_name = "Calculation"
        if not list_helper.is_null_or_empty(partition_info_list):
            partitions_str = " & ".join([partition_info.to_str() for partition_info in partition_info_list])
            calculation_name = f"Partition-{partitions_str}"
        return calculation_name

    @staticmethod
    def _get_col_metadata_list(excluded_column_names: List[str],
                               column_default_values: Dict[str, List[str]]) \
            -> List[DqColumnMetadata]:
        excluded_column_names = _get_or_default(excluded_column_names, [])
        column_default_values = _get_or_default(column_default_values, {})
        all_columns = set()
        all_columns.update(excluded_column_names)
        all_columns.update(list(column_default_values.keys()))
        ret_list = []
        for col in all_columns:
            inclusion_flag = None
            if excluded_column_names is not None and col in excluded_column_names:
                inclusion_flag = False
            act_meta = DqColumnMetadata()
            act_meta.column_name = col
            act_meta.inclusion_flag = inclusion_flag
            act_meta.default_values = column_default_values[col] if col in column_default_values else None
            ret_list.append(act_meta)
        return ret_list

    @classmethod
    def _get_input_source_settings(cls, index_of_calc: int, settings: UserInputSourceSettings,
                                   partition_info_list: List[UserPartitionInfo],
                                   included_column_names: List[str]) \
            -> Union[DqDfInputSourceSettings, DqFileInputSourceSettings]:

        if isinstance(settings.source, str):
            record_source = DqFileRecordSource(locator=settings.source)
            act_settings = DqFileInputSourceSettings(record_source)
            act_settings.csv_separator = _get_or_default(settings.csv_separator, ",")
            act_settings.number_of_rows_per_step = _get_or_default(settings.number_of_rows_per_step, 1000000)
            act_settings.date_columns = settings.date_columns
        elif isinstance(settings.source, pd.DataFrame):
            name = settings.name
            if is_null_or_empty(name):
                name = f"Input Source of Calculation-{index_of_calc + 1}"
            record_source = DqDfRecordSource(locator=settings.source, name=name)
            act_settings = DqDfInputSourceSettings(record_source)
        else:
            raise ValueError("Invalid input source type!")

        act_settings.sampling_ratio = _get_or_default(settings.sampling_ratio, 1.0)
        act_settings.is_sampling_on = act_settings.sampling_ratio != 1.0
        act_settings.max_num_of_samples = _get_or_default(settings.max_num_of_samples, sys.maxsize)
        act_settings.partition_info_list = cls._get_partition_info_list(partition_info_list)
        act_settings.included_columns = included_column_names
        act_settings.filter_callable = settings.filter_callable
        return act_settings

    @classmethod
    def _get_partition_info_list(cls, user_partition_info_list: List[UserPartitionInfo]) -> List[PartitionInfo]:
        if user_partition_info_list is None:
            return []
        ret_list = []
        for user_info in user_partition_info_list:
            partition_info = PartitionInfo()
            partition_info.column_name = user_info.column_name
            partition_info.column_values = cls.__get_partition_info_column_values(user_info.column_values)
            ret_list.append(partition_info)
        return ret_list

    @classmethod
    def __get_partition_info_column_values(cls, column_values: Union[List[float], List[str],
                                                                     List[UserDateValueDefinition]]):
        new_list = []
        for val in column_values:
            new_val = val
            if isinstance(val, UserDateValueDefinition):
                new_val = DateValueDefinition(year=val.year, month=val.month, day=val.day, hour=val.hour)
            new_list.append(new_val)
        return new_list

    def __get_comp_params(self, calculation_count: int):
        comp_params = self._get_comp_param_instance()
        input_comp = self._user_input
        comp_params.comparison_columns = self.__get_comparison_columns(input_comp.column_benchmark_horizons,
                                                                       input_comp.duplicate_control_columns)
        comp_params.test_groups = BaseUserInputService.__get_test_groups_info(input_comp.excluded_test_groups,
                                                                              input_comp.test_group_benchmark_horizons,
                                                                              calculation_count)
        comp_params.z_score = _get_or_default(input_comp.z_score, DqConstants.Z_SCORE_DEFAULT)
        comp_params.psi_threshold_green = _get_or_default(input_comp.psi_threshold_green,
                                                          DqConstants.PSI_THRESHOLD_GREEN)
        comp_params.psi_threshold_yellow = _get_or_default(input_comp.psi_threshold_yellow,
                                                           DqConstants.PSI_THRESHOLD_YELLOW)
        comp_params.traffic_light_threshold_green = _get_or_default(input_comp.traffic_light_threshold_green,
                                                                    DqConstants.TRAFFIC_LIGHT_THRESHOLD_GREEN)
        comp_params.traffic_light_threshold_yellow = _get_or_default(input_comp.traffic_light_threshold_yellow,
                                                                     DqConstants.TRAFFIC_LIGHT_THRESHOLD_YELLOW)
        comp_params.minimum_cardinality = _get_or_default(input_comp.minimum_cardinality,
                                                          DqConstants.MINIMUM_CARDINALITY_DEFAULT)
        comp_params.maximum_nom_cardinality = _get_or_default(input_comp.maximum_nom_cardinality,
                                                              DqConstants.CONTROL_MAXIMUM_NOM_CARDINALITY_DEFAULT)
        return comp_params

    @staticmethod
    def __get_test_groups_info(excluded_test_groups: List[str],
                               test_group_benchmark_horizons: Dict[str, int],
                               calculation_count: int) -> List[DqTestGroup]:

        default_test_gr_info = BaseUserInputService.__get_default_test_group_info_as_dict(calculation_count)
        if excluded_test_groups is not None:
            for group in excluded_test_groups:
                gr_type = BaseUserInputService.__get_enum_value(group, DqTestGroupType, "test group type")
                default_test_gr_info[gr_type].inclusion_flag = False
        if test_group_benchmark_horizons is not None:
            for group, bmh in test_group_benchmark_horizons.items():
                gr_type = BaseUserInputService.__get_enum_value(group, DqTestGroupType, "test group type")
                default_test_gr_info[gr_type].test_bmh = bmh
        return list(default_test_gr_info.values())

    @staticmethod
    def __get_default_test_group_info_as_dict(calculation_count: int) -> Dict[DqTestGroupType, DqTestGroup]:
        test_groups = [BaseUserInputService.__get_test_group(DqTestGroupType.RULE_BASED_CONTROLS_COLUMN_SET,
                                                             True, 0, calculation_count - 1),
                       BaseUserInputService.__get_test_group(DqTestGroupType.RULE_BASED_CONTROLS_TABLE_SET,
                                                             True, 0, calculation_count - 1),
                       BaseUserInputService.__get_test_group(DqTestGroupType.TABLE_SCHEMA_CONTROLS,
                                                             True, 1, calculation_count - 1),
                       BaseUserInputService.__get_test_group(DqTestGroupType.TRAFFIC_LIGHT_CONTROLS,
                                                             True, 1, calculation_count - 1),
                       BaseUserInputService.__get_test_group(DqTestGroupType.DISTRIBUTIONAL_COMPARISONS,
                                                             True, 1, calculation_count - 1),
                       BaseUserInputService.__get_test_group(DqTestGroupType.MODELLING_AND_CI_CONTROLS_COLUMN_SET,
                                                             True, 5, calculation_count - 1),
                       BaseUserInputService.__get_test_group(DqTestGroupType.MODELLING_AND_CI_CONTROLS_TABLE_SET,
                                                             True, 5, calculation_count - 1)]

        return {info.group_type: info for info in test_groups}

    @staticmethod
    def __get_test_group(gr_type: DqTestGroupType, inclusion_flag: bool, min_bmh: int, test_bmh: int):
        group = DqTestGroup()
        group.group_type = gr_type
        group.inclusion_flag = inclusion_flag
        group.min_bmh = min_bmh
        group.test_bmh = test_bmh
        return group

    @staticmethod
    def __get_enum_value(val_str: str, enum_type, definition: str):
        if val_str is None:
            return None
        valid_strs = [val.name for val in enum_type]
        if val_str not in valid_strs:
            raise ValueError(f"'{val_str}' is not a valid value for {definition}. Valid values are : {valid_strs}")
        return enum_type[val_str]

    @staticmethod
    def __get_comparison_columns(column_benchmark_horizons: Dict[str, int], duplicate_control_columns: List[str]) \
            -> Optional[List[DqComparisonColumnInfo]]:
        comparison_cols = []
        duplicate_control_columns = _get_or_default(duplicate_control_columns, [])
        column_benchmark_horizons = _get_or_default(column_benchmark_horizons, {})
        all_columns = set()
        all_columns.update(list(column_benchmark_horizons.keys()))
        all_columns.update(duplicate_control_columns)
        for col in all_columns:
            act_col = DqComparisonColumnInfo()
            act_col.column_name = col
            act_col.duplicate_column_control = col in duplicate_control_columns
            act_col.benchmark_horizon = column_benchmark_horizons[col] if col in column_benchmark_horizons else None
            comparison_cols.append(act_col)
        return comparison_cols

    @abc.abstractmethod
    def _get_source_type(self) -> DqRecordSourceType:
        """Returns dq source type"""

    def _get_full_proc_input_instance(self):
        source_type = self._source_type
        if source_type == DqRecordSourceType.TEXT:
            inp = DqFileFullProcessInput()
        elif source_type == DqRecordSourceType.DATA_FRAME:
            inp = DqDfFullProcessInput()
        else:
            raise ValueError("Invalid input source type!")
        return inp

    def _get_calc_param_instance(self) -> Union[DqDfCalculationParameters, DqFileCalculationParameters]:
        source_type = self._source_type
        if source_type == DqRecordSourceType.TEXT:
            inp = DqFileCalculationParameters()
        elif source_type == DqRecordSourceType.DATA_FRAME:
            inp = DqDfCalculationParameters()
        else:
            raise ValueError("Invalid input source type!")
        return inp

    def _get_comp_param_instance(self) -> Union[DqFileComparisonParameters, DqDfComparisonParameters]:
        source_type = self._source_type
        if source_type == DqRecordSourceType.TEXT:
            inp = DqFileComparisonParameters()
        elif source_type == DqRecordSourceType.DATA_FRAME:
            inp = DqDfComparisonParameters()
        else:
            raise ValueError("Invalid input source type!")
        return inp
