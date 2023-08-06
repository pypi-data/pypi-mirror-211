"""
This module includes BaseAfeSettingsReader class.
"""
from datetime import datetime
from typing import Union, List, Dict, TypeVar, Generic

import numpy as np
import pandas as pd

from organon.afe.domain.common.reader_helper import set_defaults_from_dict, setattr_if_none
from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType
from organon.afe.domain.enums.afe_learning_type import AfeLearningType
from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.modelling.supervised.afe_supervised_algorithm_settings import AfeSupervisedAlgorithmSettings
from organon.afe.domain.modelling.unsupervised.afe_unsupervised_algorithm_settings import \
    AfeUnsupervisedAlgorithmSettings
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.afe_data_settings import AfeDataSettings
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.afe_modelling_settings import AfeModellingSettings
from organon.afe.domain.settings.afe_output_settings import AfeOutputSettings
from organon.afe.domain.settings.afe_process_settings import AfeProcessSettings
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.afe_target_column import AfeTargetColumn
from organon.afe.domain.settings.auto_column_decider_settings import AutoColumnDeciderSettings
from organon.afe.domain.settings.base_afe_modelling_settings import BaseAfeModellingSettings
from organon.afe.domain.settings.base_afe_scoring_settings import BaseAfeScoringSettings
from organon.afe.domain.settings.base_afe_settings import BaseAfeSettings
from organon.afe.domain.settings.binary_target import BinaryTarget
from organon.afe.domain.settings.db_object_input import DbObjectInput
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.model_settings import ModelSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.afe.domain.settings.temporal_grid import TemporalGrid
from organon.afe.domain.settings.trx_descriptor import TrxDescriptor
from organon.fl.core.helpers import environment_info_helper

T = TypeVar("T", bound=BaseAfeModellingSettings)


class BaseAfeSettingsReader(Generic[T]):
    """
    Class for static methods on reading AfeModellingSettings from a file
    """

    def assign_default_values(self, modelling_settings: T):
        """
        Assigns default values to given AfeModellingSettings instance
        :param modelling_settings: AfeModellingSettings instance
        :type modelling_settings: BaseAfeModellingSettings
        """
        default_values_dict = self._get_default_values_dict()
        if modelling_settings.data_source_settings.auto_column_decider_settings is None:
            modelling_settings.data_source_settings.auto_column_decider_settings = AutoColumnDeciderSettings()

        set_defaults_from_dict(modelling_settings, default_values_dict)

        self.__set_binary_target_defaults(modelling_settings)

        self._set_algorithm_settings_defaults(modelling_settings)

        self._set_trx_descriptor_defaults(modelling_settings)
        self.__set_target_descriptor_defaults(modelling_settings)

        self._assign_base_afe_settings_defaults(modelling_settings)

    @classmethod
    def _get_default_values_dict(cls):
        return {
            "data_source_settings": {
                "entity_table_existence": False,
                "max_number_of_target_samples": 100000,
                "max_number_of_transaction_samples": np.iinfo(np.int64).max,
                "number_of_retry_for_empty_transaction": 10,
                "retry_interval_seconds_for_empty_transaction": 600,
                "auto_column_decider_settings": {
                    "sampling_ratio": 0.01,
                    "numeric_to_dimension": 5,
                    "dimension_distinct_cut_off": 0.95,
                    "use_dimension_columns": False,
                    "rejected_dimension_columns": [],
                    "use_quantity_columns": False,
                    "rejected_quantity_columns": []
                }
            },
            "output_settings": {
                "output_folder": "AfeOutput",
                "feature_name_prefix": "FTR",
                "enable_feature_lookup_output_to_csv": True,
                "enable_write_output": False,
                "enable_feature_space_output": False,
                "return_all_afe_columns": False,
                "enable_all_feature_lookup_output_to_csv": False
            }
        }

    @staticmethod
    def __set_binary_target_defaults(modelling_settings: T):
        try:
            target_column = modelling_settings.data_source_settings.target_descriptor.target_column
            if target_column.binary_target_info is None:
                target_column.binary_target_info = BinaryTarget()
            binary_target_info = target_column.binary_target_info
            if binary_target_info.positive_category is None and binary_target_info.negative_category is None \
                    and binary_target_info.indeterminate_category is None \
                    and binary_target_info.exclusion_category is None:
                binary_target_info.positive_category = "P"
                binary_target_info.negative_category = "N"
                binary_target_info.indeterminate_category = "I"
                binary_target_info.exclusion_category = "X"
        except AttributeError:
            pass

    def _set_algorithm_settings_defaults(self, modelling_settings: T):
        is_supervised = modelling_settings.afe_learning_type == AfeLearningType.Supervised
        if modelling_settings.algorithm_settings is None:
            if is_supervised:
                modelling_settings.algorithm_settings = AfeSupervisedAlgorithmSettings()
            else:
                modelling_settings.algorithm_settings = AfeUnsupervisedAlgorithmSettings()

        defaults = {
            "dimension_compression_ratio": 1.0,
            "dimension_max_cardinality": 200
        }
        set_defaults_from_dict(modelling_settings.algorithm_settings, defaults)

        if is_supervised:
            self.__set_supervised_algorithm_settings_defaults(modelling_settings)
        else:
            self.__set_unsupervised_algorithm_settings_defaults(modelling_settings)

    @staticmethod
    def __set_supervised_algorithm_settings_defaults(modelling_settings: T):

        defaults = {
            "training_percentage": 0.8,
            "min_data_in_leaf_and_sample_size_control_ratio": 0.1
        }
        model_defaults = {
            "model_params": {
                "learning_rate": 0.01,
                "n_estimators": 200,
                "min_data_in_leaf": 1
            },
            "model_fit_params": {
                "early_stopping_rounds": 5
            },
            "reduction_coverage": 0.5

        }
        final_model_defaults = {
            "model_params": {
                "learning_rate": 0.01,
                "n_estimators": 200,
                "min_data_in_leaf": 1
            },
            "model_fit_params": {
                "early_stopping_rounds": 5
            },
            "reduction_coverage": 0.5

        }

        algorithm_settings: AfeSupervisedAlgorithmSettings = modelling_settings.algorithm_settings
        set_defaults_from_dict(algorithm_settings, defaults)

        if algorithm_settings.model_settings is None:
            algorithm_settings.model_settings = ModelSettings()
        set_defaults_from_dict(algorithm_settings.model_settings, model_defaults)

        if algorithm_settings.final_model_settings is None:
            algorithm_settings.final_model_settings = ModelSettings()
        set_defaults_from_dict(algorithm_settings.final_model_settings, final_model_defaults)

    @staticmethod
    def __set_unsupervised_algorithm_settings_defaults(modelling_settings: T):
        defaults = {
            "bin_count": 4,
            "r_factor": 0.9,
            "max_column_count": 500,
            "is_logging": False
        }
        set_defaults_from_dict(modelling_settings.algorithm_settings, defaults)

    def _set_trx_descriptor_defaults(self, modelling_settings: T):
        # pylint: disable=no-self-use
        try:
            trx_descriptor = modelling_settings.data_source_settings.trx_descriptor
            if trx_descriptor.reading_settings is None:
                trx_descriptor.reading_settings = AfeDataReadingSettings()

            setattr_if_none(trx_descriptor.reading_settings, "number_of_rows_per_step", 100000)

        except AttributeError:
            pass

    @staticmethod
    def __set_target_descriptor_defaults(modelling_settings: T):
        try:
            target_descriptor = modelling_settings.data_source_settings.target_descriptor
            if target_descriptor.reading_settings is None:
                target_descriptor.reading_settings = AfeDataReadingSettings()

            setattr_if_none(target_descriptor.reading_settings, "number_of_rows_per_step", 100000)

        except AttributeError:
            pass

    def assign_default_values_for_scoring(self, scoring_settings: BaseAfeScoringSettings):
        """Assigns default values to scoring settings."""
        if scoring_settings.trx_reading_settings is None:
            scoring_settings.trx_reading_settings = AfeDataReadingSettings(number_of_rows_per_step=100000)

        self._assign_base_afe_settings_defaults(scoring_settings)

    @staticmethod
    def _assign_base_afe_settings_defaults(settings: BaseAfeSettings):
        """
        Assigns default values to given BaseAfeSettings instance
        :param settings: BaseAfeSettings instance
        :type settings: BaseAfeSettings
        """
        num_cores = environment_info_helper.get_total_cores()
        defaults_dict = {
            "process_settings": {
                "number_of_cores": num_cores - 1 if num_cores != 1 else 1
            }
        }
        if settings.process_settings is None:
            settings.process_settings = AfeProcessSettings()
        set_defaults_from_dict(settings, defaults_dict)

    @staticmethod
    def get_date_column(date_column_name: str = None,
                        date_column_type: Union[str, AfeDateColumnType] = None,
                        date_column_format: str = None,
                        date_column_db_format: str = None):
        """Generates AfeDateColumn instance"""
        if date_column_name is None:
            return None
        return AfeDateColumn(column_name=date_column_name, date_column_type=date_column_type,
                             custom_format=date_column_format, db_custom_format=date_column_db_format)

    def get_feature_generation_setting(self,
                                       temporal_grids: List[Union[TemporalGrid, Dict]] = None,
                                       date_resolution: Union[DateResolution, str] = None,
                                       date_column_name: str = None,
                                       date_column_type: Union[str, AfeDateColumnType] = None,
                                       date_column_format: str = None,
                                       dimension_columns: List[str] = None,
                                       quantity_columns: List[str] = None,
                                       included_operators: List[Union[AfeOperator, str]] = None,
                                       date_offset: int = None,
                                       max_observation_date: datetime = None
                                       ) -> FeatureGenerationSettings:
        """
        Generates FeatureGenerationSettings instance.
        """

        # pylint: disable=too-many-arguments

        date_column = self.get_date_column(date_column_name=date_column_name,
                                           date_column_type=date_column_type,
                                           date_column_format=date_column_format)

        return FeatureGenerationSettings(temporal_grids=temporal_grids,
                                         date_resolution=date_resolution,
                                         date_column=date_column,
                                         dimension_columns=dimension_columns,
                                         quantity_columns=quantity_columns,
                                         included_operators=included_operators,
                                         date_offset=date_offset,
                                         max_observation_date=max_observation_date
                                         )

    @staticmethod
    def get_auto_column_decider_settings(sampling_ratio: float,
                                         numeric_to_dimension: int,
                                         dimension_distinct_cut_off: float,
                                         use_dimension_columns: bool,
                                         rejected_dimension_columns: List[str],
                                         use_quantity_columns: bool,
                                         rejected_quantity_columns: List[str]):
        """Generates AutoColumnDeciderSettings instance"""
        return AutoColumnDeciderSettings(sampling_ratio=sampling_ratio,
                                         numeric_to_dimension=numeric_to_dimension,
                                         dimension_distinct_cut_off=dimension_distinct_cut_off,
                                         use_dimension_columns=use_dimension_columns,
                                         rejected_dimension_columns=rejected_dimension_columns,
                                         use_quantity_columns=use_quantity_columns,
                                         rejected_quantity_columns=rejected_quantity_columns)

    def get_trx_descriptor(self, source: Union[Dict, DbObjectInput, pd.DataFrame, str] = None,
                           entity_column_name: str = None,
                           feature_gen_setting: Union[FeatureGenerationSettings, Dict] = None,
                           number_of_rows_per_step: int = None) -> TrxDescriptor:
        """
        Generates TrxDescriptor instance for AfeModelling.
        """
        raw_input_source = RecordSource(source=source) if source is not None else None
        reading_settings = AfeDataReadingSettings(number_of_rows_per_step=number_of_rows_per_step)
        if feature_gen_setting is not None:
            if isinstance(feature_gen_setting, list):
                if len(feature_gen_setting) > 1:
                    raise ValueError("Execution with multiple feature generation settings is "
                                     "available only in premium version.")
                feature_gen_setting = feature_gen_setting[0]
            if isinstance(feature_gen_setting, dict):
                feature_gen_setting = self.get_feature_generation_setting(**feature_gen_setting)

        trx_desc = TrxDescriptor(modelling_raw_input_source=raw_input_source,
                                 entity_column_name=entity_column_name,
                                 feature_gen_setting=feature_gen_setting,
                                 reading_settings=reading_settings)
        return trx_desc

    @staticmethod
    def get_target_column(target_column_name: str = None,
                          target_column_type: Union[str, AfeTargetColumnType] = None,
                          target_positive_category: str = None,
                          target_negative_category: str = None,
                          target_indeterminate_category: str = None,
                          target_exclusion_category: str = None):
        """Generates AfeTargetColumn instance"""
        if target_column_name is None:
            return None
        return AfeTargetColumn(column_name=target_column_name,
                               target_column_type=target_column_type,
                               binary_target_info=BinaryTarget(positive_category=target_positive_category,
                                                               negative_category=target_negative_category,
                                                               indeterminate_category=target_indeterminate_category,
                                                               exclusion_category=target_exclusion_category))

    def get_target_descriptor(
            self,
            entity_column_name: str,
            date_column_name: str = None,
            date_column_type: Union[str, AfeDateColumnType] = None,
            date_column_format: str = None,
            date_column_db_format: str = None,
            target_column_name: str = None,
            target_column_type: Union[str, AfeTargetColumnType] = None,
            target_positive_category: str = None,
            target_negative_category: str = None,
            target_indeterminate_category: str = None,
            target_exclusion_category: str = None,
            default_measurement_date: datetime = None,
            number_of_rows_per_step: int = None
    ) -> TargetDescriptor:
        """
        Generates TargetDescriptor instance for AfeModelling.
        """
        # pylint: disable=too-many-arguments
        date_column = self.get_date_column(date_column_name=date_column_name,
                                           date_column_type=date_column_type,
                                           date_column_format=date_column_format,
                                           date_column_db_format=date_column_db_format)
        target_column = self.get_target_column(target_column_name=target_column_name,
                                               target_column_type=target_column_type,
                                               target_positive_category=target_positive_category,
                                               target_negative_category=target_negative_category,
                                               target_indeterminate_category=target_indeterminate_category,
                                               target_exclusion_category=target_exclusion_category)
        reading_settings = AfeDataReadingSettings(number_of_rows_per_step=number_of_rows_per_step)
        return TargetDescriptor(entity_column_name=entity_column_name,
                                date_column=date_column,
                                target_column=target_column,
                                default_measurement_date=default_measurement_date,
                                reading_settings=reading_settings)

    @staticmethod
    def get_supervised_algorithm_settings(training_percentage: float = None,
                                          min_data_in_leaf_and_sample_size_control_ratio: float = None,
                                          dimension_compression_ratio: float = None,
                                          dimension_max_cardinality: int = None,
                                          reduction_coverage: float = None,
                                          model_params: Dict = None,
                                          model_fit_params: Dict = None,
                                          final_reduction_coverage: float = None,
                                          final_model_params: Dict = None,
                                          final_model_fit_params: Dict = None,
                                          ):
        """
        Generates AfeSupervisedAlgorithmSettings instance.
        """
        # pylint: disable=too-many-arguments
        alg_settings: AfeSupervisedAlgorithmSettings = AfeSupervisedAlgorithmSettings(
            training_percentage=training_percentage,
            min_data_in_leaf_and_sample_size_control_ratio=min_data_in_leaf_and_sample_size_control_ratio,
            dimension_compression_ratio=dimension_compression_ratio,
            dimension_max_cardinality=dimension_max_cardinality
        )
        model_settings = ModelSettings(model_params=model_params, model_fit_params=model_fit_params,
                                       reduction_coverage=reduction_coverage)
        final_model_settings = ModelSettings(model_params=final_model_params, model_fit_params=final_model_fit_params,
                                             reduction_coverage=final_reduction_coverage)
        alg_settings.model_settings = model_settings
        alg_settings.final_model_settings = final_model_settings
        return alg_settings

    @staticmethod
    def get_unsupervised_algorithm_settings(bin_count: int = None,
                                            r_factor: float = None,
                                            max_column_count: int = None,
                                            is_logging: bool = None,
                                            dimension_compression_ratio: float = None,
                                            dimension_max_cardinality: int = None
                                            ):
        """
        Returns AfeUnsupervisedAlgorithmSettings instance.
        """
        # pylint: disable=too-many-arguments
        return AfeUnsupervisedAlgorithmSettings(
            bin_count=bin_count,
            r_factor=r_factor,
            max_column_count=max_column_count,
            is_logging=is_logging,
            dimension_compression_ratio=dimension_compression_ratio,
            dimension_max_cardinality=dimension_max_cardinality
        )

    @staticmethod
    def get_output_settings(output_folder: str = None,
                            output_prefix: str = None,
                            feature_name_prefix: str = None,
                            enable_feature_lookup_output_to_csv: bool = None,
                            enable_write_output: bool = None,
                            return_all_afe_columns: bool = None,
                            enable_all_feature_lookup_output_to_csv: bool = None
                            ):
        """Generates AfeOutputSettings instance"""
        # pylint: disable=too-many-arguments
        return AfeOutputSettings(output_folder=output_folder, output_prefix=output_prefix,
                                 feature_name_prefix=feature_name_prefix,
                                 enable_feature_lookup_output_to_csv=enable_feature_lookup_output_to_csv,
                                 enable_write_output=enable_write_output,
                                 return_all_afe_columns=return_all_afe_columns,
                                 enable_all_feature_lookup_output_to_csv=enable_all_feature_lookup_output_to_csv
                                 )

    def get_settings(
            self,
            trx_descriptor: Union[TrxDescriptor, Dict] = None,
            target_descriptor: Union[TargetDescriptor, Dict] = None,
            target_record_source_list: List[Union[str, pd.DataFrame]] = None,
            output_settings: Union[AfeOutputSettings, Dict] = None,
            scoring_raw_input_source: Union[Dict, DbObjectInput, str, pd.DataFrame] = None,
            scoring_target_source: Union[Dict, DbObjectInput, str, pd.DataFrame] = None,
            afe_learning_type: Union[str, AfeLearningType] = None,
            algorithm_settings: AfeAlgorithmSettings = None,
            auto_column_decider_settings: AutoColumnDeciderSettings = None,
            number_of_cores: int = None,
            max_number_of_transaction_samples: int = None,
            max_number_of_target_samples: int = None,
            entity_table_existence: bool = None
    ) -> AfeModellingSettings:
        """
        Generates AfeModellingSettings instance.
        """
        # pylint: disable=too-many-arguments
        scoring_raw_input_source = RecordSource(
            source=scoring_raw_input_source) if scoring_raw_input_source is not None else None
        scoring_target_source = RecordSource(
            source=scoring_target_source) if scoring_target_source is not None else None
        if target_record_source_list is not None:
            target_record_source_list = [RecordSource(source=obj) for obj in target_record_source_list]

        process_settings = AfeProcessSettings(number_of_cores=number_of_cores)

        if trx_descriptor is not None and isinstance(trx_descriptor, dict):
            trx_descriptor = self.get_trx_descriptor(**trx_descriptor)

        if target_descriptor is not None:
            if isinstance(target_descriptor, dict):
                target_descriptor = self.get_target_descriptor(**target_descriptor)

        if output_settings is not None:
            if isinstance(output_settings, Dict):
                output_settings = self.get_output_settings(**output_settings)
        else:
            output_settings = AfeOutputSettings()

        modelling_settings = AfeModellingSettings()
        modelling_settings.data_source_settings = AfeDataSettings(
            trx_descriptor=trx_descriptor,
            target_descriptor=target_descriptor,
            target_record_source_list=target_record_source_list,
            auto_column_decider_settings=auto_column_decider_settings,
            max_number_of_target_samples=max_number_of_target_samples,
            max_number_of_transaction_samples=max_number_of_transaction_samples
        )

        modelling_settings.data_source_settings.entity_table_existence = entity_table_existence
        modelling_settings.scoring_raw_input_source = scoring_raw_input_source
        modelling_settings.scoring_target_source = scoring_target_source
        modelling_settings.algorithm_settings = algorithm_settings
        modelling_settings.process_settings = process_settings
        modelling_settings.output_settings = output_settings
        modelling_settings.afe_learning_type = afe_learning_type
        return modelling_settings

    @classmethod
    def _get_default_included_afe_operators(cls) -> List[AfeOperator]:
        return [AfeOperator.Density, AfeOperator.Sum, AfeOperator.Frequency, AfeOperator.TimeSinceFirst,
                AfeOperator.Ratio]
