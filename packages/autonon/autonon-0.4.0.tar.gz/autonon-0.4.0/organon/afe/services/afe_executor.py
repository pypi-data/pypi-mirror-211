"""
This module includes AfeExecutionHelper class.
"""
from datetime import datetime
from typing import Union, List, Dict, Optional, Tuple, TypeVar, Generic

import pandas as pd

import organon
from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.domain.common.persist_helper import PersistHelper
from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType
from organon.afe.domain.enums.afe_learning_type import AfeLearningType
from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.modelling.supervised.multi_target_modelling_service import MultiTargetModellingService
from organon.afe.domain.modelling.unsupervised.unsupervised_feature_extraction_service import \
    UnsupervisedFeatureExtractionService
from organon.afe.domain.reporting.afe_matplotlib_report_helper import AfeMatplotlibReportHelper
from organon.afe.domain.reporting.afe_plotly_report_helper import AfePlotlyReportHelper
from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput
from organon.afe.domain.reporting.base_report_helper import BaseReportHelper
from organon.afe.domain.scoring.afe_scoring_service import AfeScoringService
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.afe_modelling_settings import AfeModellingSettings
from organon.afe.domain.settings.afe_output_settings import AfeOutputSettings
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.afe_scoring_settings import AfeScoringSettings
from organon.afe.domain.settings.afe_settings_reader import AfeSettingsReader
from organon.afe.domain.settings.afe_settings_validator import AfeSettingsValidator
from organon.afe.domain.settings.auto_column_decider_settings import AutoColumnDeciderSettings
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.afe.domain.settings.temporal_grid import TemporalGrid
from organon.afe.domain.settings.trx_descriptor import TrxDescriptor
from organon.afe.services.afe_application_operations import AfeApplicationOperations
from organon.common.helpers import dev_mode_helper
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import process_info_helper
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.fl.serialization.serialization_helper import serialize_to_file, deserialize_from_file

AfeModelOutputType = TypeVar("AfeModelOutputType", bound=BaseAfeModelOutput)


class AFE(Generic[AfeModelOutputType]):
    """
    AfeExecutionHelper class
    """

    def __init__(self):
        self._initialize_afe()
        self.model_output: Optional[AfeModelOutputType] = None
        self._settings_reader = self._get_afe_settings_reader()

    @classmethod
    def init_dev_mode(cls, log_to_console: bool = True, log_file: str = "application.log"):
        """Initializes development mode."""
        dev_mode_helper.init_dev_mode(organon.afe.__name__, log_to_console=log_to_console, log_file=log_file)

    @classmethod
    def _initialize_afe(cls):
        AfeApplicationOperations.initialize_app()

    @classmethod
    def _get_afe_settings_reader(cls):
        return AfeSettingsReader()

    @classmethod
    def _get_afe_settings_validator(cls):
        return AfeSettingsValidator()

    def fit(self, settings: AfeModellingSettings) -> AfeModelOutputType:
        """
        Runs Automated Feature Extraction modelling.

        :param settings: AfeModellingSettings instance
        :return: AfeModelOutputType instance
        """
        if not isinstance(settings, AfeModellingSettings):
            raise ValueError("Please give an AfeModellingSettings.")

        modelling_input = settings

        self.model_output = self._run_afe_modelling(modelling_input)

        LogHelper.info("Afe modelling finished successfully.")
        return self.model_output

    def transform(self, trx_source: Union[pd.DataFrame, str],
                  target_source: Union[pd.DataFrame, str] = None,
                  for_date: str or int or datetime = None,
                  num_threads: int = None,
                  trx_reading_settings: Union[AfeDataReadingSettings, Dict] = None,
                  **kwargs):
        """
        Runs Automated Feature Extraction scoring.

        :param trx_source: Transaction record source
        :param target_source: Target records to score
        :param for_date: If given, scoring will be done for only this date
        :param num_threads: Number of threads to use for scoring(cpu_count-1 by default)
        :param trx_reading_settings: Reading settings for trx_source
        :return: Score dataframe
        """
        # pylint: disable=too-many-arguments,unused-argument
        self._check_model_output()
        return self.transform_model(self.model_output, trx_source, target_source=target_source,
                                    for_date=for_date,
                                    num_threads=num_threads,
                                    trx_reading_settings=trx_reading_settings)

    def persist_model(self, location: str):
        """
        Saves model output to given location.

        :param location: file path or db table object.
        """
        self._check_model_output()
        self.persist_model_output(self.model_output, location)

    def load_model(self, location: str, secret_key: str = None, **kwargs):
        """
        Loads model output from given location

        :param location: file path
        :param secret_key: secret key generated while saving model
        """
        # pylint:disable=unused-argument
        self.model_output = self.get_model(location, secret_key=secret_key, **kwargs)

    def show_afe_report(self, use_lib="matplotlib"):
        """
        Shows afe report dashboard.

        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        self._check_model_output()
        self.create_afe_report(self.model_output, use_lib=use_lib)

    def show_feature_report(self, use_lib="matplotlib"):
        """
        Shows afe report dashboard.

        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        self._check_model_output()
        self.create_feature_report(self.model_output, use_lib=use_lib)

    def get_features_data_frame(self) -> pd.DataFrame:
        """
        Returns afe features as dataframe.

        :return:
        """
        self._check_model_output()
        return self.create_features_data_frame(self.model_output)

    def get_all_features_data_frame(self) -> pd.DataFrame:
        """
        Returns all generated afe features as dataframe.

        :return:
        """
        self._check_model_output()
        return self.create_all_features_data_frame(self.model_output)

    def show_extended_feature_report(self, use_lib="matplotlib"):
        """
        Shows extended feature report.

        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        self._check_model_output()
        self.create_extended_feature_report(self.model_output, use_lib=use_lib)

    def show_feature_importance_report(self, target_source_index: int = None,
                                       first_x_features: int = None, use_lib="matplotlib"):
        """
        Shows importance of afe features generated for given target.

        :param first_x_features: Number of columns to show in plot
        :param target_source_index: Index of target(In modelling target_record_source_list)
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        self._check_model_output()
        self.create_feature_importance_report(self.model_output, target_source_index, first_x_features, use_lib=use_lib)

    def get_feature_importance_for_targets(self) -> List[pd.DataFrame]:
        """
        Returns importance of afe features generated for all targets.

        :return: List of pandas dataframes storing feature importance data for targets
        """
        self._check_model_output()
        return self.generate_feature_importance_report_for_targets(self.model_output)

    def get_auc_score_for_targets(self, target_index: int = None) -> List[Tuple[int, float]]:
        """
        Returns auc score for all targets.
        :param target_index: Index of target(In modelling target_record_source_list)
        :return: List of float storing auc score for targets
        """
        self._check_model_output()
        return self.generate_auc_score_for_targets(self.model_output, target_index)

    def show_resource_usage_report(self, use_lib="matplotlib"):
        """
        Shows resource usage dashboard.

        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        self._check_model_output()
        self.create_resource_usage_report(self.model_output, use_lib=use_lib)

    def show_roc_curve_report(self, target_source_index: int = None, target_class=None,
                              use_lib="matplotlib"):
        """
        Shows roc_curve for given target.

        :param target_source_index: Index of target(In modelling target_record_source_list)
        :param target_class: target class to report roc_curve for (if multiclass afe modelling)
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        self._check_model_output()
        self.create_roc_curve_report(self.model_output, target_source_index, target_class=target_class, use_lib=use_lib)

    def _check_model_output(self):
        if self.model_output is None:
            raise KnownException("No model has been generated before")

    @classmethod
    def transform_model(cls, model_output: AfeModelOutputType, trx_source: Union[pd.DataFrame, str],
                        target_source: Union[pd.DataFrame, str] = None,
                        for_date: str or int or datetime = None,
                        num_threads: int = None,
                        trx_reading_settings: Union[AfeDataReadingSettings, Dict] = None, **kwargs):
        """
        Runs Automated Feature Extraction scoring for given model output.

        :param model_output: AfeModelOutputType instance to score
        :param trx_source: Transaction record source
        :param target_source: Target records to score
        :param for_date: If given, scoring will be done for only this date
        :param num_threads: Number of threads to use for scoring(cpu_count-1 by default)
        :param trx_reading_settings: Reading settings for trx_source
        :return: Score dataframe
        """
        # pylint: disable=too-many-arguments,unused-argument
        scoring_settings = AfeScoringSettings()

        scoring_settings.model_output = model_output
        if target_source is not None:
            scoring_settings.target_record_source = RecordSource(source=target_source)
        else:
            if for_date is None:
                raise KnownException("Please enter either target_source or for_date parameters to transform.")
        scoring_settings.raw_input_source = RecordSource(source=trx_source)

        if trx_reading_settings is not None:
            scoring_settings.trx_reading_settings = trx_reading_settings \
                if isinstance(trx_reading_settings, AfeDataReadingSettings) \
                else AfeDataReadingSettings(**trx_reading_settings)
        score_df = cls._run_afe_scoring(scoring_settings, num_threads=num_threads, for_date=for_date)
        return score_df

    @classmethod
    def _run_afe_modelling(cls, settings: AfeModellingSettings):
        """Runs afe modelling with given settings"""
        cls._get_afe_settings_validator().validate_modelling_settings(settings)
        cls._get_afe_settings_reader().assign_default_values(settings)

        if settings.afe_learning_type == AfeLearningType.Supervised:
            service = MultiTargetModellingService(settings)
        elif settings.afe_learning_type == AfeLearningType.Unsupervised:
            service = UnsupervisedFeatureExtractionService(settings)
        else:
            raise NotImplementedError

        return service.execute()

    @classmethod
    def _run_afe_scoring(cls, settings: AfeScoringSettings, num_threads: int = None, for_date=None, **kwargs) \
            -> Optional[pd.DataFrame]:
        """Runs afe scoring with given settings"""
        # pylint: disable=unused-argument

        cls._get_afe_settings_validator().validate_scoring_settings(settings)
        cls._get_afe_settings_reader().assign_default_values_for_scoring(settings)

        service = AfeScoringService(settings)

        return service.score(num_threads, for_date=for_date)

    @classmethod
    def get_feature_generation_setting(cls,
                                       temporal_grids: List[Union[TemporalGrid, Dict]] = None,
                                       date_resolution: Union[DateResolution, str] = None,
                                       date_column_name: str = None,
                                       date_column_type: Union[str, AfeDateColumnType] = None,
                                       date_column_format: str = None,
                                       dimension_columns: List[str] = None,
                                       quantity_columns: List[str] = None,
                                       included_operators: List[Union[AfeOperator, str]] = None,
                                       date_offset: int = None,
                                       max_observation_date: datetime = None,
                                       **kwargs
                                       ):
        """
        Generates FeatureGenerationSettings instance.

        :param temporal_grids:
        :param date_resolution:
        :param date_column_name:
        :param date_column_type:
        :param date_column_format:
        :param dimension_columns:
        :param quantity_columns:
        :param included_operators:
        :param date_offset:
        :param max_observation_date:
        :return:
        """
        # pylint: disable=too-many-arguments, unused-argument
        return cls._get_afe_settings_reader().get_feature_generation_setting(
            temporal_grids=temporal_grids,
            date_resolution=date_resolution,
            date_column_name=date_column_name,
            date_column_format=date_column_format,
            date_column_type=date_column_type,
            dimension_columns=dimension_columns,
            quantity_columns=quantity_columns,
            included_operators=included_operators,
            date_offset=date_offset,
            max_observation_date=max_observation_date
        )

    @classmethod
    def get_auto_column_decider_setting(cls, sampling_ratio: float = None,
                                        numeric_to_dimension: int = None,
                                        dimension_distinct_cut_off: float = None,
                                        use_dimension_columns: bool = None,
                                        rejected_dimension_columns: List[str] = None,
                                        use_quantity_columns: bool = None,
                                        rejected_quantity_columns: List[str] = None):
        """
        Generates AutoColumnDeciderSettings instance.

        :param sampling_ratio:
        :param numeric_to_dimension:
        :param dimension_distinct_cut_off:
        :param use_dimension_columns:
        :param rejected_dimension_columns:
        :param use_quantity_columns:
        :param rejected_quantity_columns:
        :return:
        """
        # pylint: disable=too-many-arguments, unused-argument
        return cls._get_afe_settings_reader().get_auto_column_decider_settings(
            sampling_ratio=sampling_ratio,
            numeric_to_dimension=numeric_to_dimension,
            dimension_distinct_cut_off=dimension_distinct_cut_off,
            use_dimension_columns=use_dimension_columns,
            rejected_dimension_columns=rejected_dimension_columns,
            use_quantity_columns=use_quantity_columns,
            rejected_quantity_columns=rejected_quantity_columns
        )

    @classmethod
    def get_trx_descriptor(cls,
                           source: Union[pd.DataFrame, str],
                           entity_column_name: str,
                           feature_generation_settings: Union[FeatureGenerationSettings, Dict],
                           number_of_rows_per_step: int = None) -> TrxDescriptor:
        """
        Generates TrxDescriptor instance for AfeModelling.

        :param source: Transaction record source
        :param entity_column_name: Name of column storing entity ids
        :param feature_generation_settings: Feature generation settings
        :param number_of_rows_per_step: Size of chunks to read in memory while reading target record source
        :return: Transaction record source descriptor
        """
        return cls._get_afe_settings_reader().get_trx_descriptor(
            source=source,
            entity_column_name=entity_column_name,
            feature_gen_setting=feature_generation_settings,
            number_of_rows_per_step=number_of_rows_per_step
        )

    @classmethod
    def get_target_descriptor(cls,
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
                              number_of_rows_per_step: int = None) -> TargetDescriptor:
        """
        Generates TargetDescriptor instance for AfeModelling.


        :param target_column_name:
        :param target_column_type:
        :param target_positive_category:
        :param target_negative_category:
        :param target_indeterminate_category:
        :param target_exclusion_category:
        :param entity_column_name: Name of column storing entity ids
        :param date_column_name: Name of column storing event dates
        :param date_column_type:
        :param date_column_format:
        :param date_column_db_format:
        :param default_measurement_date:
        :param number_of_rows_per_step: Size of chunks to read in memory while reading target record source
        :return: Target record source descriptor
        """
        # pylint: disable=too-many-arguments
        return cls._get_afe_settings_reader().get_target_descriptor(
            entity_column_name=entity_column_name,
            date_column_name=date_column_name,
            date_column_type=date_column_type,
            date_column_format=date_column_format,
            date_column_db_format=date_column_db_format,
            target_column_name=target_column_name,
            target_column_type=target_column_type,
            target_positive_category=target_positive_category,
            target_negative_category=target_negative_category,
            target_indeterminate_category=target_indeterminate_category,
            target_exclusion_category=target_exclusion_category,
            default_measurement_date=default_measurement_date,
            number_of_rows_per_step=number_of_rows_per_step)

    @classmethod
    def get_supervised_algorithm_settings(cls,
                                          training_percentage: float = None,
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

        :param training_percentage: percentage of data to be used as training data
        :param min_data_in_leaf_and_sample_size_control_ratio:
        :param dimension_compression_ratio:
        :param dimension_max_cardinality:
        :param reduction_coverage:
        :param model_params:
        :param model_fit_params:
        :param final_reduction_coverage:
        :param final_model_params:
        :param final_model_fit_params:
        :return:
        """
        # pylint: disable=too-many-arguments
        return cls._get_afe_settings_reader().get_supervised_algorithm_settings(
            training_percentage=training_percentage,
            min_data_in_leaf_and_sample_size_control_ratio=min_data_in_leaf_and_sample_size_control_ratio,
            dimension_compression_ratio=dimension_compression_ratio,
            dimension_max_cardinality=dimension_max_cardinality,
            model_params=model_params,
            model_fit_params=model_fit_params,
            reduction_coverage=reduction_coverage,
            final_model_params=final_model_params,
            final_model_fit_params=final_model_fit_params,
            final_reduction_coverage=final_reduction_coverage
        )

    @classmethod
    def get_unsupervised_algorithm_settings(cls,
                                            bin_count: int = None,
                                            r_factor: float = None,
                                            max_column_count: int = None,
                                            is_logging: bool = None,
                                            dimension_compression_ratio: float = None,
                                            dimension_max_cardinality: int = None
                                            ):
        """
        Returns AfeUnsupervisedAlgorithmSettings instance.

        :param bin_count:
        :param r_factor:
        :param max_column_count:
        :param is_logging:
        :param dimension_compression_ratio:
        :param dimension_max_cardinality:
        :return:
        """
        # pylint: disable=too-many-arguments
        return cls._get_afe_settings_reader().get_unsupervised_algorithm_settings(
            bin_count=bin_count,
            r_factor=r_factor,
            max_column_count=max_column_count,
            is_logging=is_logging,
            dimension_compression_ratio=dimension_compression_ratio,
            dimension_max_cardinality=dimension_max_cardinality
        )

    @classmethod
    def get_output_settings(cls,
                            output_folder: str = None,
                            output_prefix: str = None,
                            feature_name_prefix: str = None,
                            enable_feature_lookup_output_to_csv: bool = None,
                            enable_write_output: bool = None,
                            return_all_afe_columns: bool = None,
                            enable_all_feature_lookup_output_to_csv: bool = None,
                            **kwargs):
        """
        Generates AfeOutputSettings instance

        :param output_folder:
        :param output_prefix:
        :param feature_name_prefix:
        :param enable_feature_lookup_output_to_csv:
        :param enable_write_output:
        :return:
        """
        # pylint: disable=too-many-arguments,unused-argument
        return cls._get_afe_settings_reader().get_output_settings(
            output_folder=output_folder, output_prefix=output_prefix,
            feature_name_prefix=feature_name_prefix,
            enable_feature_lookup_output_to_csv=enable_feature_lookup_output_to_csv,
            enable_write_output=enable_write_output,
            return_all_afe_columns=return_all_afe_columns,
            enable_all_feature_lookup_output_to_csv=enable_all_feature_lookup_output_to_csv
        )

    @classmethod
    def get_settings(cls,
                     trx_descriptor: Union[TrxDescriptor, Dict],
                     target_descriptor: Union[TargetDescriptor, Dict],
                     target_record_source_list: List[Union[str, pd.DataFrame]],
                     afe_learning_type: Union[str, AfeLearningType],
                     output_settings: Union[AfeOutputSettings, Dict] = None,
                     algorithm_settings: AfeAlgorithmSettings = None,
                     auto_column_decider_settings: AutoColumnDeciderSettings = None,
                     number_of_cores: int = None,
                     max_number_of_transaction_samples: int = None,
                     max_number_of_target_samples: int = None,
                     **kwargs
                     ):
        """
        Generates AfeModellingSettings instance.

        :param trx_descriptor:
        :param target_descriptor:
        :param target_record_source_list:
        :param output_settings:
        :param afe_learning_type:
        :param algorithm_settings:
        :param auto_column_decider_settings:
        :param number_of_cores: Maximum number of cores to be used while modelling
        :param max_number_of_target_samples:
        :param max_number_of_transaction_samples:
        :return:
        """
        # pylint: disable=too-many-arguments, unused-argument
        return cls._get_afe_settings_reader().get_settings(
            trx_descriptor, target_descriptor, target_record_source_list, output_settings,
            None, None, afe_learning_type,
            algorithm_settings, auto_column_decider_settings, number_of_cores, max_number_of_transaction_samples,
            max_number_of_target_samples)

    @classmethod
    def persist_model_output(cls, model_output: AfeModelOutputType, location: str):
        """
        Saves model output to given location.

        :param model_output:
        :param location: file path
        """
        if not isinstance(location, str):
            raise ValueError("Location invalid. Enter a file path.")
        serialize_to_file(model_output, location, secret_key=AfeStaticObjects.get_secret_key())

    @classmethod
    def get_model(cls, location: str, secret_key: str = None, **kwargs) -> AfeModelOutputType:
        """
        Loads model output from given location

        :param location: file path.
        :param secret_key: secret key generated while saving model
        """
        # pylint: disable=unused-argument
        if not isinstance(location, str):
            raise NotImplementedError("Location invalid. Enter a file path.")
        secret_key = secret_key if secret_key is not None else AfeStaticObjects.get_secret_key()
        return deserialize_from_file(location, secret_key=secret_key)

    @staticmethod
    def get_process_peak_memory_usage():
        """Returns peak memory usage of process in bytes"""
        return process_info_helper.get_peak_memory_usage()

    @classmethod
    def create_afe_report(cls, model_output: AfeModelOutputType, use_lib="matplotlib"):
        """
        Shows afe report dashboard.

        :param model_output:
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        report_helper: BaseReportHelper = cls._get_report_helper(use_lib)
        report = report_helper.generate_afe_report(model_output)
        report_helper.generate_afe_report_dashboard(report)

    @classmethod
    def create_feature_report(cls, model_output: AfeModelOutputType, use_lib="matplotlib"):
        """
        Shows afe features dashboard.

        :param model_output:
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        report_helper: BaseReportHelper = cls._get_report_helper(use_lib)
        report = report_helper.generate_afe_report(model_output)
        report_helper.generate_afe_feature_dashboard(report)

    @classmethod
    def create_resource_usage_report(cls, model_output: AfeModelOutputType, use_lib="matplotlib"):
        """
        Shows resource usage dashboard.

        :param model_output:
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        report_helper: BaseReportHelper = cls._get_report_helper(use_lib)
        report = report_helper.generate_afe_report(model_output)
        report_helper.generate_resource_usage_dashboard(report)

    @classmethod
    def create_extended_feature_report(cls, model_output: AfeModelOutputType, use_lib="matplotlib"):
        """
        Shows extended feature report.

        :param model_output:
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        report_helper: BaseReportHelper = cls._get_report_helper(use_lib)
        report = report_helper.generate_afe_report(model_output)
        report_helper.generate_feature_extended_dashboard(report)

    @classmethod
    def create_feature_importance_report(cls, model_output: AfeModelOutputType, target_source_index: int = None,
                                         first_x_features: int = None, use_lib="matplotlib"):
        """
        Shows importance of afe features generated for given target.

        :param model_output:
        :param first_x_features: Number of columns to show in plot
        :param target_source_index: Index of target(In modelling target_record_source_list)
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        if model_output.afe_learning_type == AfeLearningType.Unsupervised:
            raise KnownException("Feature importance report is not available on Unsupervised models.")
        report_helper: BaseReportHelper = cls._get_report_helper(use_lib)
        report = report_helper.generate_afe_report(model_output)
        report_helper.generate_feature_importance_dashboard(report, target_index=target_source_index,
                                                            first_x_feature=first_x_features)

    @staticmethod
    def generate_feature_importance_report_for_targets(model_output: AfeModelOutputType) -> List[pd.DataFrame]:
        """
        Returns importance of afe features generated for all targets.

        :param model_output:
        :return: List of pandas dataframes storing feature importance data for targets
        """
        if model_output.afe_learning_type == AfeLearningType.Unsupervised:
            raise KnownException("Feature importance report is not available on Unsupervised models.")
        importance_data_list = []
        if model_output.final_column_metrics is None:
            raise ValueError("afe report does not include final column metrics")
        for metrics in model_output.final_column_metrics:
            data = metrics["feature_importances"].sort_values(by="Value", ascending=False)
            importance_data_list.append(data)
        return importance_data_list

    @staticmethod
    def generate_auc_score_for_targets(model_output: AfeModelOutputType, target_index: int = None) -> List[
        Tuple[int, float]]:
        """
         Returns auc score for all targets.
        :param model_output:
        :return: List of float storing auc score for targets

        """
        if model_output.afe_learning_type == AfeLearningType.Unsupervised:
            raise KnownException("AUC score is not available on Unsupervised models.")
        if model_output.final_column_metrics is None:
            raise ValueError("afe report does not include final column metrics")
        metrics_to_report = list(enumerate(model_output.final_column_metrics))
        auc_score_list = []

        if target_index is not None:
            if len(model_output.final_column_metrics) <= target_index:
                raise KnownException(f"Target with index {target_index} does not exist. "
                                     f"Num targets: {len(model_output.final_column_metrics)}")
            auc_score_list.append((target_index, model_output.final_column_metrics[target_index]["auc"]["all"]))
        else:
            for i, metrics in metrics_to_report:
                auc = metrics["auc"]["all"]
                auc_score_list.append((i, auc))
        return auc_score_list

    @classmethod
    def create_roc_curve_report(cls, model_output: AfeModelOutputType, target_source_index: int = None,
                                target_class=None, use_lib="matplotlib"):
        """
        Shows roc_curve for given target.

        :param model_output:
        :param target_source_index: Index of target(In modelling target_record_source_list)
        :param target_class: target class report roc_curve for (if multiclass afe modelling)
        :param use_lib: Visualization library to use. Valid values: "matplotlib", "plotly"
        """
        if model_output.afe_learning_type == AfeLearningType.Unsupervised:
            raise KnownException("ROC report is not available on Unsupervised models.")
        report_helper: BaseReportHelper = cls._get_report_helper(use_lib)
        report = report_helper.generate_afe_report(model_output)
        report_helper.generate_roc_curve_dashboard(report, target_index=target_source_index, target_class=target_class)

    @classmethod
    def create_features_data_frame(cls, model_output: AfeModelOutputType):
        """
        Returns afe features as dataframe.

        :param model_output:
        :return:
        """
        return PersistHelper.get_lookup_data_frame(list(model_output.output_features.values()),
                                                   model_output.transaction_file_stats)

    @classmethod
    def create_all_features_data_frame(cls, model_output: AfeModelOutputType):
        """
        Returns all generated afe features as dataframe.

        :param model_output:
        :return:
        """
        return PersistHelper.get_lookup_data_frame(list(model_output.all_features.values()),
                                                   model_output.transaction_file_stats)

    @classmethod
    def _get_report_helper(cls, use_lib="matplotlib") -> BaseReportHelper:
        return AfeMatplotlibReportHelper() if use_lib == "matplotlib" else AfePlotlyReportHelper()

    @staticmethod
    def set_secret_key(secret_key: str):
        """Sets secret key for encryption tasks used during serialization etc."""

        AfeStaticObjects.set_secret_key(secret_key)
