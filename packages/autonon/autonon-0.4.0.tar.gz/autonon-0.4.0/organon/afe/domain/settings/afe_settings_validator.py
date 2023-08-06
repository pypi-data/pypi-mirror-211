"""
This module includes AfeSettingsValidator class.
"""
from typing import List, Dict

import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType
from organon.afe.domain.enums.afe_learning_type import AfeLearningType
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.afe.domain.modelling.supervised.afe_supervised_algorithm_settings import AfeSupervisedAlgorithmSettings
from organon.afe.domain.modelling.unsupervised.afe_unsupervised_algorithm_settings import \
    AfeUnsupervisedAlgorithmSettings
from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.afe_output_settings import AfeOutputSettings
from organon.afe.domain.settings.afe_settings_type_validators import validate_types_modelling_settings, \
    validate_types_scoring_settings
from organon.afe.domain.settings.afe_target_column import AfeTargetColumn
from organon.afe.domain.settings.base_afe_data_settings import BaseAfeDataSettings
from organon.afe.domain.settings.base_afe_modelling_settings import BaseAfeModellingSettings
from organon.afe.domain.settings.base_afe_scoring_settings import BaseAfeScoringSettings
from organon.afe.domain.settings.base_trx_descriptor import BaseTrxDescriptor
from organon.afe.domain.settings.db_object_input import DbObjectInput
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.afe.domain.settings.temporal_grid import TemporalGrid
from organon.afe.domain.settings.trx_descriptor import TrxDescriptor
from organon.afe.domain.settings.validation_helper import check_required_attrs, raise_or_add_exception
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import list_helper, string_helper


class AfeSettingsValidator:
    """
    This class have static methods to validate AfeModellingSettings object before Automated Feature Extraction process
     either by raising exceptions or returning a list of exceptions
    """

    def __init__(self):
        self._columns_per_source: Dict[RecordSource, List[str]] = {}

    def validate_modelling_settings(self, modelling_settings: BaseAfeModellingSettings):
        """
        Validate AfeModellingSettings object by raising exceptions
        :param modelling_settings: AfeModellingSettings object to be validated.
        :type modelling_settings: BaseAfeModellingSettings
        """
        validate_types_modelling_settings(modelling_settings)
        self.validate_afe_modelling_settings_requirements(modelling_settings)

    def validate_scoring_settings(self, scoring_settings: BaseAfeScoringSettings):
        """
        Validate AfeModellingSettings object by raising exceptions
        :param scoring_settings: AfeModellingSettings object to be validated.
        :type scoring_settings: BaseAfeModellingSettings
        """
        validate_types_scoring_settings(scoring_settings)
        self.validate_afe_scoring_settings_requirements(scoring_settings)

    def get_modelling_validation_errors(self, modelling_settings: BaseAfeModellingSettings) -> List[Exception]:
        """
        Validate AfeModellingsSettings to return a list of exceptions that should have been raised during validation.
        :param modelling_settings: AfeModellingSettings object to be validated.
        :type modelling_settings: BaseAfeModellingSettings
        :return:
        """
        exc_list = validate_types_modelling_settings(modelling_settings, exception_list=True)
        exc_list.extend(self.validate_afe_modelling_settings_requirements(modelling_settings, exception_list=True))
        return exc_list

    @staticmethod
    def _get_horizon_list(temporal_grids: List[TemporalGrid]) -> List[int]:
        """
        Creates horizonlist from given TemporalGrid
        :param temporal_grids: List of TemporalGrid instances
        :type temporal_grids: List[TemporalGrid]
        :return: horizon list
        """
        ret_list = set()
        for temporal_grid in temporal_grids:
            for i in range(temporal_grid.length):
                ret_list.add(temporal_grid.offset + i * temporal_grid.stride)
        return list(ret_list)

    @classmethod
    def validate_afe_model_output_requirements(cls, obj: BaseAfeModelOutput, obj_str: str = "model_output",
                                               exception_list: bool = False) \
            -> List[Exception]:
        """
        Validates requirements of AfeScoringSettings object.
        :param obj: Object to be validated.
        :type obj: BaseAfeModelOutput
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["output_features", "transaction_file_stats", "trx_entity_column", "trx_date_columns",
                          "target_descriptor"]
        exc_list.extend(check_required_attrs(obj, required_attrs, obj_str, exception_list=exception_list))
        return exc_list

    def validate_afe_scoring_settings_requirements(self, obj: BaseAfeScoringSettings, exception_list: bool = False) \
            -> List[Exception]:
        """
        Validates requirements of AfeScoringSettings object.
        :param obj: Object to be validated.
        :type obj: PAfeScoringSettings
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["model_output", "raw_input_source"]
        exc_list.extend(check_required_attrs(obj, required_attrs, "", exception_list=exception_list))

        if obj.model_output is not None:
            exc_list.extend(self.validate_afe_model_output_requirements(obj.model_output, "model_output",
                                                                        exception_list=exception_list))

        if obj.raw_input_source is not None:
            if obj.raw_input_source.get_type() not in [RecordSourceType.TEXT, RecordSourceType.DATA_FRAME]:
                exc = KnownException("Scoring raw input source should be either a DataFrame or file path")
                raise_or_add_exception(exc, exc_list=exc_list, add_to_list=exception_list)
            exc_list.extend(self.validate_record_source_requirements(obj.raw_input_source, "raw_input_source",
                                                                     exception_list=exception_list))

        if obj.target_record_source is not None:
            if obj.target_record_source.get_type() not in [RecordSourceType.TEXT, RecordSourceType.DATA_FRAME]:
                exc = KnownException("Scoring target source should be either a DataFrame or file path")
                raise_or_add_exception(exc, exc_list=exc_list, add_to_list=exception_list)
            exc_list.extend(self.validate_record_source_requirements(obj.target_record_source, "target_record_source",
                                                                     exception_list=exception_list))

        return exc_list

    def validate_afe_modelling_settings_requirements(self, obj: BaseAfeModellingSettings,
                                                     exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeModellingSettings object.
        :param obj: Object to be validated.
        :type obj: BaseAfeModellingSettings
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["data_source_settings", "afe_learning_type"]
        exc_list.extend(check_required_attrs(obj, required_attrs, "", exception_list=exception_list))

        if obj.afe_learning_type is not None:
            if obj.afe_learning_type == AfeLearningType.Supervised:
                if obj.algorithm_settings is not None:
                    exc_list.extend(
                        self.validate_supervised_algorithm_settings_requirements(obj.algorithm_settings,
                                                                                 "supervised_algorithm_settings",
                                                                                 exception_list=exception_list))

            elif obj.afe_learning_type == AfeLearningType.Unsupervised:
                if obj.algorithm_settings is not None:
                    exc_list.extend(
                        self.validate_unsupervised_algorithm_settings_requirements(obj.algorithm_settings,
                                                                                   "unsupervised_algorithm_settings",
                                                                                   exception_list=exception_list))
            if obj.data_source_settings is not None:
                exc_list.extend(
                    self.validate_data_source_requirements(
                        obj.data_source_settings, "data_source_settings",
                        is_supervised=obj.afe_learning_type == AfeLearningType.Supervised,
                        exception_list=exception_list))

        if obj.output_settings is not None:
            exc_list.extend(
                self.validate_output_settings_requirements(obj.output_settings, "output_settings",
                                                           exception_list=exception_list))

        return exc_list

    def validate_data_source_requirements(self, obj: BaseAfeDataSettings, obj_str: str = "data_source_settings",
                                          is_supervised: bool = False, exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeDataSettings object.
        :param is_supervised: Is the setting supervised?
        :param obj: Object to be validated.
        :type obj: BaseAfeDataSettings
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["trx_descriptor", "target_descriptor",
                          "target_record_source_list"]

        if obj.trx_descriptor is not None \
                and obj.trx_descriptor.modelling_raw_input_source is not None \
                and obj.trx_descriptor.modelling_raw_input_source.get_type() == RecordSourceType.DATABASE:
            required_attrs.append("entity_table")

        exc_list.extend(check_required_attrs(obj, required_attrs, obj_str, exception_list=exception_list))

        if obj.trx_descriptor is not None:
            exc_list.extend(
                self.validate_trx_descriptor_requirements(obj.trx_descriptor,
                                                          f"{obj_str}.trx_descriptor",
                                                          exception_list=exception_list))

        if obj.target_descriptor is not None:
            exc_list.extend(self.validate_target_descriptor_requirements(obj.target_descriptor,
                                                                         f"{obj_str}.target_descriptor",
                                                                         is_supervised,
                                                                         obj.target_record_source_list,
                                                                         exception_list=exception_list))

        if obj.target_record_source_list is not None:
            if len(obj.target_record_source_list) == 0:
                exc = KnownException(f"{obj_str}.target_record_source_list cannot be empty.")
                raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
            else:
                for i, record_source in enumerate(obj.target_record_source_list):
                    exc_list.extend(self.validate_record_source_requirements(
                        record_source,
                        f"{obj_str}.target_record_source_list[{i}]",
                        exception_list=exception_list))

        return exc_list

    def validate_trx_descriptor_requirements(self, obj: BaseTrxDescriptor,
                                             obj_str: str = "trx_descriptor",
                                             exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of TransactionFileDesciptor object.
        :param obj: Object to be validated.
        :type obj: BaseTrxDescriptor
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []

        if not isinstance(obj, TrxDescriptor):
            raise ValueError

        required_attrs = ["modelling_raw_input_source", "entity_column_name", "feature_gen_setting"]
        feature_generation_setting = obj.feature_gen_setting

        exc_list.extend(check_required_attrs(obj, required_attrs, obj_str, exception_list=exception_list))

        if not string_helper.is_null_or_empty(obj.entity_column_name):
            exc_list.extend(self._check_column_in_source(obj.entity_column_name, obj.modelling_raw_input_source,
                                                         "transaction source",
                                                         exception_list=exception_list))

        if obj.modelling_raw_input_source is not None:
            mod_raw_inp_src_exc = self.validate_record_source_requirements(obj.modelling_raw_input_source,
                                                                           f"{obj_str}.modelling_raw_input_source",
                                                                           exception_list=exception_list)

            exc_list.extend(mod_raw_inp_src_exc)

        if feature_generation_setting is not None:
            exc_list.extend(
                self.validate_afe_feature_generation_settings_requirements(
                    feature_generation_setting,
                    f"{obj_str}.feature_gen_setting",
                    raw_input_source=obj.modelling_raw_input_source,
                    exception_list=exception_list))

        return exc_list

    @classmethod
    def validate_record_source_requirements(cls, obj: RecordSource, obj_str: str = "record_source",
                                            exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of RecordSource object.
        :param obj: Object to be validated.
        :type obj: RecordSource
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["source"]
        exc_list.extend(check_required_attrs(obj, required_attrs, obj_str, exception_list))
        if obj.get_type() == RecordSourceType.DATABASE and obj.source is not None:
            exc_list.extend(
                cls.validate_db_object_input_requirements(obj.source, f"{obj_str}.source", exception_list))
        return exc_list

    def validate_target_descriptor_requirements(self, obj: TargetDescriptor,
                                                obj_str: str = "target_descriptor",
                                                is_supervised: bool = False,
                                                target_record_source_list: List[RecordSource] = None,
                                                exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of TargetFileDescriptor object.
        :param is_supervised: If algorithm supervised then target_column is needed
        :param obj: Object to be validated.
        :type obj: TargetDescriptor
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["entity_column_name"]
        if is_supervised:
            required_attrs.append("target_column")

        columns_to_check = []
        required_attr_exceptions = check_required_attrs(obj, required_attrs, obj_str, exception_list)
        exc_list.extend(required_attr_exceptions)
        self._add_if_not_null_or_empty(obj.entity_column_name, columns_to_check)
        if obj.date_column is not None:
            date_col_exc = self.validate_afe_date_column_requirements(obj.date_column, f"{obj_str}.date_column",
                                                                      exception_list=exception_list)
            exc_list.extend(date_col_exc)
            self._add_if_not_null_or_empty(obj.date_column.column_name, columns_to_check)
            exc_list.extend(
                self._validate_date_column_for_target_source_list(obj.date_column, target_record_source_list,
                                                                  f"{obj_str}.date_column", exception_list))

        if is_supervised and obj.target_column is not None:
            target_col_exc = self.validate_afe_target_column_requirements(obj.target_column,
                                                                          f"{obj_str}.target_column",
                                                                          exception_list=exception_list)
            exc_list.extend(target_col_exc)
            self._add_if_not_null_or_empty(obj.target_column.column_name, columns_to_check)

        if not is_supervised and obj.target_column is not None:
            exc = KnownException(f"{obj_str}.target_column should be None for unsupervised modelling.")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)

        if target_record_source_list is not None:
            for i, source in enumerate(target_record_source_list):
                for col in columns_to_check:
                    exc_list.extend(self._check_column_in_source(col, source, f"target_record_source_list[{i}]"))

        return exc_list

    def validate_afe_feature_generation_settings_requirements(self, obj: FeatureGenerationSettings,
                                                              obj_str: str = "feature_generation_settings",
                                                              raw_input_source: RecordSource = None,
                                                              exception_list: bool = False):
        """
        Validates requirements of AfeDateColumnSettings object.
        :param obj: Object to be validated.
        :type obj: FeatureGenerationSettings
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        columns_to_check = []
        if obj.date_column is not None:
            date_col_excs = check_required_attrs(obj,
                                                 ["date_resolution", "temporal_grids"],
                                                 obj_str, exception_list)
            exc_list.extend(date_col_excs)

            date_col_exc = self.validate_afe_date_column_requirements(obj.date_column, f"{obj_str}.date_column",
                                                                      exception_list=exception_list)
            exc_list.extend(date_col_exc)
            exc_list.extend(self._validate_date_column_for_raw_input_source(obj.date_column, raw_input_source,
                                                                            f"{obj_str}.date_column",
                                                                            exception_list=exception_list))
            self._add_if_not_null_or_empty(obj.date_column.column_name, columns_to_check)
        else:
            obj.temporal_grids = [TemporalGrid(stride=1, length=1, offset=1)]
            obj.date_resolution = DateResolution.Day

        if not list_helper.is_null_or_empty(obj.temporal_grids):
            temp_grid_excs = []
            for i, temp_grid in enumerate(obj.temporal_grids):
                temp_grid_excs.extend(self.validate_temporal_grid_requirements(temp_grid,
                                                                               f"{obj_str}.temporal_grids[{i}]",
                                                                               exception_list=exception_list))
            obj.horizon_list = self._get_horizon_list(obj.temporal_grids) if len(temp_grid_excs) == 0 else None
            exc_list.extend(temp_grid_excs)
        else:
            exc = KnownException(f"{obj_str}.temporal_grids cannot be empty")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)

        if not list_helper.is_null_or_empty(obj.dimension_columns):
            columns_to_check.extend([col for col in obj.dimension_columns
                                     if col != AfeStaticObjects.empty_dimension_column])
        if not list_helper.is_null_or_empty(obj.quantity_columns):
            columns_to_check.extend([col for col in obj.quantity_columns
                                     if col != AfeStaticObjects.empty_quantity_column])

        for col in columns_to_check:
            exc_list.extend(self._check_column_in_source(col, raw_input_source,
                                                         "transaction source",
                                                         exception_list=exception_list))

        return exc_list

    @classmethod
    def validate_afe_date_column_requirements(cls, obj: AfeDateColumn, obj_str: str = "date_column",
                                              exception_list: bool = False):
        """
        Validates requirements of AfeDateColumn object.

        :param obj: Object to be validated.
        :type obj: AfeDateColumn
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        date_col_excs = check_required_attrs(obj,
                                             ["column_name", "date_column_type"],
                                             obj_str, exception_list)
        exc_list.extend(date_col_excs)
        if obj.date_column_type == AfeDateColumnType.CustomFormat:
            if obj.custom_format is None:
                exc = KnownException(f"Please provide {obj_str}.custom_format.")
                raise_or_add_exception(exc, exc_list, add_to_list=exception_list)

        return exc_list

    @classmethod
    def validate_afe_target_column_requirements(cls, obj: AfeTargetColumn, obj_str: str = "target_column",
                                                exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeTargetColumn object.
        :param obj: Object to be validated.
        :type obj: AfeTargetColumn
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["column_name", "target_column_type"]
        target_col_exc = check_required_attrs(obj, required_attrs,
                                              obj_str, exception_list)
        exc_list.extend(target_col_exc)

        if obj.target_column_type == AfeTargetColumnType.Binary:
            binary_target_info = obj.binary_target_info
            if binary_target_info is not None:
                bin_target_fields = [binary_target_info.positive_category, binary_target_info.negative_category,
                                     binary_target_info.indeterminate_category, binary_target_info.exclusion_category]

                if bin_target_fields[0] is None or bin_target_fields[1] is None or \
                        sum(x is not None for x in bin_target_fields) == 3:
                    exc = KnownException(f"{obj_str}.binary_target_info is invalid.")
                    raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
            else:
                exc = KnownException(f"{obj_str}.binary_target_info should be provided.")
                raise_or_add_exception(exc, exc_list, add_to_list=exception_list)

        return exc_list

    @classmethod
    def validate_supervised_algorithm_settings_requirements(cls, obj: AfeSupervisedAlgorithmSettings,
                                                            obj_str: str = "supervised_algorithm_settings",
                                                            exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeSupervisedAlgorithmSettings object.
        :param obj: Object to be validated.
        :type obj: AfeSupervisedAlgorithmSettings
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        exc_list.extend(cls.validate_afe_algorithm_settings_requirements(obj, obj_str, exception_list=exception_list))

        return exc_list

    @classmethod
    def validate_unsupervised_algorithm_settings_requirements(cls, obj: AfeUnsupervisedAlgorithmSettings,
                                                              obj_str: str = "unsupervised_algorithm_settings",
                                                              exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeUnsupervisedAlgorithmSettings object.
        :param obj: Object to be validated.
        :type obj: AfeUnsupervisedAlgorithmSettings
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        exc_list.extend(cls.validate_afe_algorithm_settings_requirements(obj, obj_str, exception_list=exception_list))
        return exc_list

    @classmethod
    def validate_output_settings_requirements(cls, obj: AfeOutputSettings, obj_str: str = "output_settings",
                                              exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeOutputSettings object.
        :param obj: Object to be validated.
        :type obj: AfeOutputSettings
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        output_params = [obj.enable_all_feature_lookup_output_to_csv, obj.enable_feature_lookup_output_to_csv,
                         obj.enable_write_output]
        prefix_needed = sum([1 for val in output_params if val is True]) > 0
        if prefix_needed:
            if string_helper.is_null_or_empty(obj.output_prefix):
                exc = KnownException(f"Please give {obj_str}.output_prefix which will be used as a prefix in "
                                     f"output file names."
                                     "If you do not want your output files of a previous AFE execution to be "
                                     "overwritten, either output_folder or output_prefix should be "
                                     "given a unique value")
                raise_or_add_exception(exc, exc_list, exception_list)

        return exc_list

    @classmethod
    def validate_afe_algorithm_settings_requirements(cls, obj: AfeAlgorithmSettings,
                                                     obj_str: str = "algorithm_settings",
                                                     exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of AfeAlgorithmSettings object.
        :param obj: Object to be validated.
        :type obj: AfeAlgorithmSettings
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        # pylint: disable=unused-argument
        exc_list = []

        return exc_list

    @classmethod
    def validate_db_object_input_requirements(cls, obj: DbObjectInput, obj_str: str = "DbObjectInput",
                                              exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of DbObjectDto object.
        :param obj: Object to be validated.
        :type obj: DbObjectInput
        :param obj_str: A string to define the object
        :type obj_str: str
        :param exception_list: If true, no exceptions will be raised and a list of caught exceptions will be returned
        :type exception_list: bool
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["connection_name"]
        exc_list.extend(check_required_attrs(obj, required_attrs, obj_str, exception_list=exception_list))
        if obj.sql_statement is None and (obj.schema_name is None or obj.table_name is None):
            exc = KnownException(
                f"Either give {obj_str}.sql_statement or {obj_str}.schema_name with {obj_str}.table_name")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
        return exc_list

    @classmethod
    def validate_temporal_grid_requirements(cls, obj: TemporalGrid, obj_str: str = "TemporalGrid",
                                            exception_list: bool = False) -> List[Exception]:
        """
        Validates requirements of TemporalGrid object.
        :param TemporalGrid obj: Object to be validated.
        :param str obj_str: A string to define the object
        :param bool exception_list: If true,
            no exceptions will be raised and a list of caught exceptions will be returned
        :return: List[Exception]
        """
        exc_list = []
        required_attrs = ["length", "stride", "offset"]
        exc_list.extend(check_required_attrs(obj, required_attrs, obj_str, exception_list=exception_list))
        if obj.offset <= 0:
            exc = KnownException(f"{obj_str}.offset should be a positive integer")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
        if obj.length <= 0:
            exc = KnownException(f"{obj_str}.length should be a positive integer")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
        if obj.stride <= 0:
            exc = KnownException(f"{obj_str}.stride should be a positive integer")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
        return exc_list

    @classmethod
    def _validate_date_column_for_raw_input_source(cls, date_column: AfeDateColumn, raw_input_source: RecordSource,
                                                   obj_str: str,
                                                   exception_list: bool = False):
        # pylint: disable=unused-argument
        return []

    @classmethod
    def _validate_date_column_for_target_source_list(cls, date_column: AfeDateColumn,
                                                     target_record_source_list: List[RecordSource],
                                                     obj_str: str,
                                                     exception_list: bool = False):
        # pylint: disable=unused-argument
        return []

    def _check_column_in_source(self, column: str, source: RecordSource, source_name: str,
                                exception_list: bool = False):
        exc_list = []
        if source not in self._columns_per_source:
            self._columns_per_source[source] = self._get_columns_from_source(source)
        if column not in self._columns_per_source[source]:
            exc = KnownException(f"Column '{column}' not found in {source_name}")
            raise_or_add_exception(exc, exc_list, add_to_list=exception_list)
        return exc_list

    @classmethod
    def _get_columns_from_source(cls, source: RecordSource):
        if source.get_type() == RecordSourceType.DATA_FRAME:
            return list(source.source.columns)
        if source.get_type() == RecordSourceType.TEXT:
            return list(pd.read_csv(source.source, sep=",", nrows=0).columns)
        raise NotImplementedError

    @staticmethod
    def _add_if_not_null_or_empty(string_val: str, _list: List[str]):
        if not string_helper.is_null_or_empty(string_val):
            _list.append(string_val)
