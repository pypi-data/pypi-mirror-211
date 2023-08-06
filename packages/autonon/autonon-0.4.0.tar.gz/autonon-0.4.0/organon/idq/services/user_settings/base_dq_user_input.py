"""Includes Dq user input classes."""
from typing import List, Dict

import pandas as pd

from organon.idq.services.user_settings.user_calculation_params import UserCalculationParams
from organon.idq.services.user_settings.user_date_value_definition import UserDateValueDefinition
from organon.idq.services.user_settings.user_db_obj_locator import UserDbObjLocator
from organon.idq.services.user_settings.user_input_source_settings import UserInputSourceSettings
from organon.idq.services.user_settings.user_multi_partition_calculation_params import \
    UserMultiPartitionCalcParams
from organon.idq.services.user_settings.user_partition_info import UserPartitionInfo


class BaseDqUserInput:
    """User class for all dq settings"""

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.calc_params: UserMultiPartitionCalcParams = None
        self.use_supplied_calcs_as_comp_inputs: bool = None
        self.included_column_names: List[str] = None
        self.excluded_column_names: List[str] = None
        self.column_default_values: Dict[str, List[str]] = None
        self.column_benchmark_horizons: Dict[str, int] = None
        self.duplicate_control_columns: List[str] = None
        self.minimum_cardinality: int = None
        self.maximum_nom_cardinality: int = None
        self.traffic_light_threshold_yellow: float = None
        self.traffic_light_threshold_green: float = None
        self.psi_threshold_yellow: float = None
        self.psi_threshold_green: float = None
        self.z_score: float = None
        self.excluded_test_groups: List[str] = None
        self.test_group_benchmark_horizons: Dict[str, int] = None
        self.include_date_columns: bool = None

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

    def set_comparison_params(self,
                              column_benchmark_horizons: Dict[str, int] = None,
                              duplicate_control_columns: List[str] = None,
                              maximum_nom_cardinality: int = None,
                              minimum_cardinality: int = None,
                              traffic_light_threshold_yellow: float = None,
                              traffic_light_threshold_green: float = None,
                              psi_threshold_yellow: float = None,
                              psi_threshold_green: float = None,
                              z_score: float = None,
                              excluded_test_groups: List[str] = None,
                              test_group_benchmark_horizons: Dict[str, int] = None,
                              included_column_names: List[str] = None,
                              excluded_column_names: List[str] = None,
                              column_default_values: Dict[str, List[str]] = None,
                              include_date_columns: bool = None
                              ):
        """Adds comparison settings"""
        # pylint: disable=too-many-arguments
        self._check_simple_types(locals(),
                                 {
                                     "column_benchmark_horizons": dict,
                                     "duplicate_control_columns": list,
                                     "maximum_nom_cardinality": int,
                                     "minimum_cardinality": int,
                                     "traffic_light_threshold_yellow": [int, float],
                                     "traffic_light_threshold_green": [int, float],
                                     "psi_threshold_yellow": float,
                                     "psi_threshold_green": float,
                                     "z_score": [int, float],
                                     "excluded_test_groups": list,
                                     "test_group_benchmark_horizons": dict,
                                     "included_column_names": list,
                                     "excluded_column_names": list,
                                     "column_default_values": dict,
                                     "include_date_columns": bool,
                                 })

        self.maximum_nom_cardinality = maximum_nom_cardinality
        self.minimum_cardinality = minimum_cardinality
        self.traffic_light_threshold_green = traffic_light_threshold_green
        self.traffic_light_threshold_yellow = traffic_light_threshold_yellow
        self.psi_threshold_green = psi_threshold_green
        self.psi_threshold_yellow = psi_threshold_yellow
        self.z_score = z_score
        self.column_benchmark_horizons = column_benchmark_horizons
        self.duplicate_control_columns = duplicate_control_columns
        self.excluded_test_groups = excluded_test_groups
        self.test_group_benchmark_horizons = test_group_benchmark_horizons
        self.included_column_names = included_column_names
        self.excluded_column_names = excluded_column_names
        self.column_default_values = column_default_values
        self.include_date_columns = include_date_columns

    @classmethod
    def _get_multi_partition_calculation_params(cls, calc_name: str, input_source_settings: dict,
                                                max_nom_card_count: int, outlier_param,
                                                use_pop_nom_stats, partitions: List[List[dict]] = None):
        input_source_settings = cls._get_input_source_settings_from_dict(input_source_settings)

        partitions = cls._get_partitions_from_list(partitions)
        return UserMultiPartitionCalcParams(calc_name, input_source_settings, max_nom_card_count,
                                            outlier_param,
                                            use_pop_nom_stats, partitions)

    @classmethod
    def _get_calculation_params(cls, calc_name: str, input_source_settings, max_nom_card_count,
                                outlier_param,
                                use_pop_nom_stats, partition: List[dict] = None):
        input_source_settings = cls._get_input_source_settings_from_dict(input_source_settings)

        partition = cls._get_partition(partition)
        return UserCalculationParams(calc_name, input_source_settings, max_nom_card_count,
                                     outlier_param,
                                     use_pop_nom_stats, partition=partition)

    @classmethod
    def _get_partitions_from_list(cls, partitions: List[List[dict]]) -> List[List[UserPartitionInfo]]:
        if partitions is not None:
            if not isinstance(partitions, list):
                raise ValueError("partitions should be given as a list of lists")
            all_partition_lists = []
            for i, partition_info_list in enumerate(partitions):
                if not isinstance(partition_info_list, list):
                    raise ValueError("partitions should be given as a list of lists")
                new_list = []
                for j, info in enumerate(partition_info_list):
                    new_info = info
                    if isinstance(info, dict):
                        new_info = BaseDqUserInput._get_partition_info_from_dict(
                            info, f"partitions[{i}][{j}]")
                    new_list.append(new_info)
                all_partition_lists.append(new_list)
            partitions = all_partition_lists
        return partitions

    @classmethod
    def _get_partition(cls, partition_info_list: List[dict]) -> List[UserPartitionInfo]:
        if partition_info_list is None:
            return None
        if not isinstance(partition_info_list, list):
            raise ValueError("A partition should be given as a list of dicts")
        new_list = []
        for j, info in enumerate(partition_info_list):
            new_info = info
            if isinstance(info, dict):
                new_info = BaseDqUserInput._get_partition_info_from_dict(info, f"partition[{j}]")
            new_list.append(new_info)
        return new_list

    @classmethod
    def _get_input_source_settings_from_dict(cls, settings_dict: dict) -> UserInputSourceSettings:
        settings = UserInputSourceSettings()
        BaseDqUserInput._check_simple_types(settings_dict, {
            "source": [UserDbObjLocator, str, pd.DataFrame, dict],
            "name": str,
            "sampling_ratio": float,
            "max_num_of_samples": int,
            "included_columns": list,
            "number_of_rows_per_step": int,
            "partition_info_list": list,
            "date_columns": list
        })

        BaseDqUserInput._get_from_dict(settings_dict, settings, "input_source_settings")

        if settings.filter_callable is not None:
            if not callable(settings.filter_callable) or settings.filter_callable.__code__.co_argcount != 1:
                raise ValueError("'filter_callable' should be a callable which takes "
                                 "only one argument (dataframe to filter)")

        if settings.source is not None:
            if isinstance(settings.source, dict):
                locator = UserDbObjLocator()
                BaseDqUserInput._get_from_dict(settings.source, locator, "input_source_settings['source']")
                settings.source = locator
        return settings

    @staticmethod
    def _get_partition_info_from_dict(info: dict, definition_str: str):
        new_info = UserPartitionInfo()
        BaseDqUserInput._check_simple_types(info, {
            "column_name": str,
            "column_values": list
        }, definition_str)
        base_definition_str = definition_str
        BaseDqUserInput._get_from_dict(info, new_info, base_definition_str)
        if new_info.column_values is not None:
            values_list = []
            for j, value in enumerate(new_info.column_values):
                new_val = value
                if isinstance(value, dict):
                    new_val = UserDateValueDefinition()
                    BaseDqUserInput._check_simple_types(value, {
                        "year": int,
                        "month": int,
                        "day": int,
                        "hour": int
                    }, f"{base_definition_str}['column_values'][{j}]")
                    BaseDqUserInput._get_from_dict(
                        value, new_val, f"{base_definition_str}['column_values'][{j}]")
                values_list.append(new_val)
            new_info.column_values = values_list
        return new_info

    @staticmethod
    def _get_from_dict(val_dict: dict, target_obj: object, definition: str):
        if not isinstance(val_dict, dict):
            raise ValueError(f"{definition} should be given as a dict")
        for key, val in val_dict.items():
            if key not in target_obj.__dict__:
                raise ValueError(f"'{key}' is not a valid attribute for {definition}")
            setattr(target_obj, key, val)

    @staticmethod
    def _get_from_list_of_dicts(val_list: List[dict], target_type: type, elem_definition: str):
        if val_list is None:
            return None
        ret_list = []
        for val_dict in val_list:
            target_obj = target_type()
            BaseDqUserInput._get_from_dict(val_dict, target_obj, elem_definition)
            ret_list.append(target_obj)
        return ret_list

    @staticmethod
    def _check_list_of_dict(_list, description):
        if _list is not None:
            exc = f"{description} should be given as list of dicts."
            if not isinstance(_list, list):
                raise ValueError(exc)
            for val_dict in _list:
                if not isinstance(val_dict, dict):
                    raise ValueError(exc)

    @staticmethod
    def _check_simple_types(val_dict, type_dict, obj_definition: str = None):
        for param, expected_type in type_dict.items():
            param_str = param if obj_definition is None else f"{obj_definition}.{param}"
            if param not in val_dict:
                continue
            val = val_dict[param]
            if val is None:
                continue
            if isinstance(expected_type, list):
                found = False
                for exp_type in expected_type:
                    if isinstance(val, exp_type):
                        found = True
                if not found:
                    type_names = [t.__name__ for t in expected_type]
                    raise ValueError(f"{param_str} should be an instance of one of '{type_names}'")
            else:
                if not isinstance(val, expected_type):
                    raise ValueError(f"{param_str} should be an instance of '{expected_type.__name__}'")
