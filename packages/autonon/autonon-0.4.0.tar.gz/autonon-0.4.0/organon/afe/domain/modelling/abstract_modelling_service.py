"""Includes AbstractModellingService class."""
import abc
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from typing import TypeVar, Generic

import numpy as np
import pandas as pd

from organon.afe.dataaccess.services.i_sample_data_service import ISampleDataService
from organon.afe.dataaccess.services.sample_data_service import SampleDataService
from organon.afe.domain.common.base_execution_plan_service import BaseExecutionPlanService
from organon.afe.domain.common.persist_helper import PersistHelper
from organon.afe.domain.enums.afe_learning_type import AfeLearningType
from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.afe.domain.modelling.businessobjects.afe_column import AfeColumn
from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature
from organon.afe.domain.modelling.businessobjects.data_frame_builder import DataFrameBuilder
from organon.afe.domain.modelling.businessobjects.multi_target_entity_container import MultiTargetEntityContainer
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats
from organon.afe.domain.modelling.helper import trx_reader_helper
from organon.afe.domain.modelling.supervised.afe_supervised_algorithm_settings import AfeSupervisedAlgorithmSettings
from organon.afe.domain.modelling.supervised.multi_target_entity_container_service import \
    MultiTargetEntityContainerService
from organon.afe.domain.modelling.unsupervised.afe_unsupervised_algorithm_settings import \
    AfeUnsupervisedAlgorithmSettings
from organon.afe.domain.reporting.afe_column_dto import AfeColumnDto
from organon.afe.domain.reporting.base_afe_model_output import BaseAfeModelOutput
from organon.afe.domain.reporting.runtime_statistics import RuntimeStatistics
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.base_afe_modelling_settings import BaseAfeModellingSettings
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.modelling_reduction_settings import ModellingReductionSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.businessobjects.date_interval import DateInterval
from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.core.businessobjects.fl_core_static_objects import FlCoreStaticObjects
from organon.fl.core.businessobjects.idata_partition import IDataPartition
from organon.fl.core.executionutil.objects.stopwatch import StopWatch
from organon.fl.core.extensions.string_extensions import effective_value
from organon.fl.core.fileoperations import file_io_helper, directory_helper
from organon.fl.core.helpers import guid_helper, date_helper, process_info_helper
from organon.fl.logging.helpers.log_helper import LogHelper

AfeModellingSettingsType = TypeVar("AfeModellingSettingsType", bound=BaseAfeModellingSettings)
AfeModelOutputType = TypeVar("AfeModelOutputType", bound=BaseAfeModelOutput)
AfeColumnType = TypeVar("AfeColumnType", bound=AfeColumn)


class AbstractModellingService(Generic[AfeModellingSettingsType, AfeModelOutputType, AfeColumnType],
                               metaclass=abc.ABCMeta):
    """Base class for afe modelling."""

    def __init__(self, settings: AfeModellingSettingsType):
        self._settings: AfeModellingSettingsType = settings
        self._all_afe_columns: Optional[Dict[str, AfeColumnType]] = {}
        self._exec_plan_service = None

    def execute(self, num_of_threads: int = None) -> AfeModelOutputType:
        """Executes multi target afe modelling using given number of threads"""
        LogHelper.info("Afe ModellingService.Execute started")
        self._control_date_column_constraint()
        if num_of_threads is None:
            num_of_threads = self._settings.process_settings.number_of_cores

        self._exec_plan_service = self._get_exec_plan_service()

        self.__log_exec_plan()
        self._exec_plan_service.start_recording_runtime_stats(interval_in_seconds=1)
        try:
            watch = StopWatch(True)

            reduced_columns, reduction_extra_info_per_target, trx_record_collection = \
                self.__execute_until_reduction(num_of_threads)

            self._exec_plan_service.start_output()
            watch.restart()

            reduced_columns_list = list(reduced_columns.values())

            output_features = self._get_output_features(reduced_columns_list)
            all_features = self._get_output_features(list(self._all_afe_columns.values()))
            self._persist_lookup_data(output_features, trx_record_collection.transaction_file_stats)
            self._persist_all_lookup_data(all_features, trx_record_collection.transaction_file_stats)

            output_time = watch.get_elapsed_seconds(True)
            self._exec_plan_service.complete_output(output_time)

            self.__log_exec_plan()
            self._exec_plan_service.stop_recording_runtime_stats()

            runtime_stats = self._exec_plan_service.get_runtime_statistics()  # pylint:disable=assignment-from-none
            if runtime_stats is not None:
                LogHelper.info(f"CPU Time: {runtime_stats.user_cpu_time + runtime_stats.system_cpu_time} seconds")
            try:
                LogHelper.info(
                    f"Process peak memory usage: {process_info_helper.get_peak_memory_usage() / (1024 * 1024)} MB")
            except NotImplementedError:
                pass

            return self._get_model_output(output_features,
                                          all_features,
                                          trx_record_collection.transaction_file_stats,
                                          runtime_stats, reduction_extra_info_per_target)
        finally:
            self._exec_plan_service.stop_recording_runtime_stats()

    def _persist_lookup_data(self, output_features: Dict[str, BaseAfeFeature], stats: TransactionFileStats):
        output_settings = self._settings.output_settings
        write_csv = output_settings.enable_feature_lookup_output_to_csv and output_settings.enable_write_output
        if not write_csv:
            return
        lookup_data_table = self._features_to_data_frame(list(output_features.values()), stats)
        csv_data = self._feature_frame_to_csv(lookup_data_table)
        file_prefix = self._settings.output_settings.get_feature_lookup_table_name()
        self._persist_lookup_csv(file_prefix, csv_data)

    def _persist_all_lookup_data(self, all_features: Dict[str, BaseAfeFeature], stats: TransactionFileStats):
        output_settings = self._settings.output_settings
        write_csv = output_settings.enable_all_feature_lookup_output_to_csv and output_settings.enable_write_output
        if not write_csv:
            return
        lookup_data_table = self._features_to_data_frame(list(all_features.values()), stats)
        csv_data = self._feature_frame_to_csv(lookup_data_table)
        file_prefix = self._settings.output_settings.get_all_features_lookup_table_name()
        self._persist_lookup_csv(file_prefix, csv_data)

    @classmethod
    def _features_to_data_frame(cls, features: List[BaseAfeFeature], stats: TransactionFileStats) -> pd.DataFrame:
        return PersistHelper.get_lookup_data_frame(features, stats)

    def _get_exec_plan_service(self) -> BaseExecutionPlanService:
        # pylint: disable=no-self-use
        return BaseExecutionPlanService()

    def __log_exec_plan(self):
        plan = self._exec_plan_service.get_plan()  # pylint:disable=assignment-from-none
        if plan is not None:
            LogHelper.info(f"Plan is: {plan}")

    @abc.abstractmethod
    def _get_output_features(self, reduced_columns_list: List[AfeColumn]):
        """Generates afe feature instances from afe columns"""

    @abc.abstractmethod
    def _control_date_column_constraint(self):
        pass

    def __execute_until_reduction(self, num_of_threads: int) -> \
            Tuple[Dict[str, AfeColumn], dict, TransactionFileRecordCollection]:

        watch = StopWatch(True)
        LogHelper.info("Started populating multi-target-entity-container")
        self._exec_plan_service.start_get_targets()
        rejected_target_classes = None
        if self._settings.data_source_settings.target_descriptor.target_column is not None:
            binary_target_info = self._settings.data_source_settings. \
                target_descriptor.target_column.binary_target_info
            rejected_target_classes = [binary_target_info.exclusion_category,
                                       binary_target_info.indeterminate_category]
        multi_target_entity_container = self._get_multi_target_entity_container(rejected_target_classes)

        interval_per_entity_per_date_col = self._get_interval_per_entity_per_date_col(multi_target_entity_container)

        self._exec_plan_service.start_decide_columns()
        sample_service = self._get_sample_service(interval_per_entity_per_date_col)
        self._decide_dimension_and_quantity_columns(sample_service)

        decide_time = watch.get_elapsed_seconds(True)
        self._exec_plan_service.complete_decide_columns(decide_time)

        self._exec_plan_service.start_trx_file()
        data_source_settings = self._settings.data_source_settings
        trx_descriptor = data_source_settings.trx_descriptor
        all_d_cols, all_q_cols = trx_descriptor.get_all_dimension_and_quantity_columns()
        trx_file_record_collection = self._read_transactions_file(all_d_cols,
                                                                  all_q_cols,
                                                                  interval_per_entity_per_date_col,
                                                                  multi_target_entity_container.unique_entity_list)
        trx_time = watch.get_elapsed_seconds(True)
        self._exec_plan_service.complete_trx_file(trx_time)

        self._exec_plan_service.set_collections(trx_file_record_collection,
                                                multi_target_entity_container.records_per_file)

        self._exec_plan_service.calculate_reduce_time()
        self.__log_exec_plan()

        self._exec_plan_service.start_reduce()
        watch.restart()

        reduced_columns, reduction_extra_info_per_target = self.__reduce_columns(
            multi_target_entity_container.records_per_file,
            trx_file_record_collection, num_of_threads)
        reduce_time = watch.get_elapsed_seconds(True)
        self._exec_plan_service.complete_reduce(reduce_time)
        LogHelper.info(f"Reducing columns finished in {reduce_time} seconds.")
        self._exec_plan_service.save_statistics()

        return reduced_columns, reduction_extra_info_per_target, trx_file_record_collection

    def _get_multi_target_entity_container(self, rejected_target_classes) -> MultiTargetEntityContainer:
        watch = StopWatch(True)
        multi_target_entity_container_service = MultiTargetEntityContainerService(
            self._settings.data_source_settings.target_record_source_list,
            self._settings.data_source_settings.target_descriptor,
            rejected_target_classes=rejected_target_classes)
        multi_target_entity_container_service.execute()
        self.control_target_record_files(multi_target_entity_container_service)
        target_time = watch.get_elapsed_seconds(True)
        self._exec_plan_service.complete_get_targets(target_time)
        LogHelper.info(
            f"Multi-target-entity-container has been populated in {target_time} seconds")

        multi_target_entity_container = multi_target_entity_container_service.container

        data_source_settings = self._settings.data_source_settings
        multi_target_entity_container.unify_entity_list(data_source_settings.max_number_of_target_samples)

        return multi_target_entity_container

    @abc.abstractmethod
    def _decide_dimension_and_quantity_columns(self, sample_service: ISampleDataService):
        """decides dimension and quantity columns for feature generation settings"""

    def _get_sample_service(self, interval_per_entity_per_date_col: Dict[str, Dict[str, DateInterval]]):
        return SampleDataService(self._settings.data_source_settings, self._settings.algorithm_settings,
                                 interval_per_entity_per_date_column=interval_per_entity_per_date_col)

    def _get_model_output(self, output_features: Dict[str, BaseAfeFeature],
                          all_features: Dict[str, BaseAfeFeature],
                          transaction_file_stats: TransactionFileStats,
                          runtime_statistics: RuntimeStatistics,
                          reduction_extra_info_per_target: Dict[RecordSource, dict]) -> AfeModelOutputType:
        # pylint: disable=too-many-arguments
        model_output = self._get_model_output_instance()
        model_output.model_identifier = guid_helper.new_guid(32)
        model_output.build_date = datetime.now()
        model_output.output_features = output_features
        model_output.all_features = all_features
        model_output.transaction_file_stats = transaction_file_stats
        model_output.runtime_stats = runtime_statistics
        data_source_settings = self._settings.data_source_settings
        model_output.trx_entity_column = data_source_settings.trx_descriptor.entity_column_name
        model_output.trx_date_columns = self._get_non_empty_date_columns_dict()
        model_output.target_descriptor = data_source_settings.target_descriptor

        if reduction_extra_info_per_target is not None:
            final_col_metrics = []
            for target_source in self._settings.data_source_settings.target_record_source_list:
                if target_source in reduction_extra_info_per_target and \
                        "final_column_metrics" in reduction_extra_info_per_target[target_source]:
                    final_col_metrics.append(reduction_extra_info_per_target[target_source]["final_column_metrics"])
            model_output.final_column_metrics = final_col_metrics

        return model_output

    @classmethod
    def _get_model_output_instance(cls) -> AfeModelOutputType:
        return BaseAfeModelOutput()

    @abc.abstractmethod
    def _get_non_empty_date_columns_dict(self):
        """return trx date columns  which are not None as a dict"""

    @abc.abstractmethod
    def _get_interval_per_entity_per_date_col(self, multi_target_entity_container: MultiTargetEntityContainer):
        """Return interval_per_entity_per_date_col for trx read"""

    def __reduce_columns(self,
                         records_per_file: Dict[RecordSource, TargetFileRecordCollection],
                         trx_file_record_collection, num_of_threads):
        reduced_columns = {}
        reduction_extra_info_per_target = {}
        record_source_index = 0
        for record_source, target_file_record_collection in records_per_file.items():
            reduction_settings = ModellingReductionSettings()
            reduction_settings.target_record_source = record_source
            reduction_settings.target_record_source_index = record_source_index
            reduction_settings.target_file_record_collection = target_file_record_collection
            reduction_settings.trx_file_record_collection = trx_file_record_collection
            reduction_settings.num_threads = num_of_threads
            _dict, reduction_extra_info = self.__reduce(reduction_settings)
            reduction_extra_info_per_target[record_source] = reduction_extra_info
            for key, value in _dict.items():
                if key not in reduced_columns:
                    if AbstractModellingService._check_reduced_columns(reduced_columns, value):
                        value.source = self._get_afe_column_source(record_source, record_source_index)
                        reduced_columns[key] = value
            record_source_index += 1

        return reduced_columns, reduction_extra_info_per_target

    @staticmethod
    def _check_reduced_columns(reduced_columns, afe_column_to_be_checked):
        check_fields = ['dimension_name', 'operator', 'quantity_name', 'set', 'time_window',
                        'date_column', 'in_out', 'offset', 'date_resolution']
        for _, afe_column in reduced_columns.items():
            is_equals = True
            for field in check_fields:
                if getattr(afe_column_to_be_checked, field) != getattr(afe_column, field):
                    is_equals = False
                    break
            if is_equals:
                return False
        return True

    def __reduce(self, reduction_settings: ModellingReductionSettings) \
            -> Tuple[Dict[str, AfeColumn], dict]:

        frame_builder = self._get_data_frame_builder(reduction_settings.target_file_record_collection,
                                                     reduction_settings.trx_file_record_collection)

        all_columns_frame = DictDataFrame(reduction_settings.target_file_record_collection.sampled_count)

        file = self.__get_report_file(self._settings.output_settings, reduction_settings.target_record_source,
                                      reduction_settings.target_record_source_index)

        directory_helper.create(self._settings.output_settings.output_folder)

        partition = self._reduce_for_settings(frame_builder, all_columns_frame, reduction_settings, file)
        _dict, reduction_extra_info = self.__run_final_model(reduction_settings.num_threads, partition, frame_builder,
                                                             file,
                                                             reduction_settings.trx_file_record_collection,
                                                             all_columns_frame)
        if file is not None:
            file.flush()
            file.close()

        return _dict, reduction_extra_info

    def _reduce_for_settings(self, frame_builder, all_columns_frame, reduction_settings, file) -> IDataPartition:
        """Executes reduction for all date-dim-qty triplets."""
        raise NotImplementedError

    def _reduce_for_feature_gen_setting(self, frame_builder, order,
                                        feature_generation_settings: FeatureGenerationSettings,
                                        reduction_settings, all_columns_frame, partition, file):
        # pylint: disable=too-many-arguments
        watch = StopWatch(start=True)
        algorithm_settings: AfeAlgorithmSettings = self._settings.algorithm_settings

        if feature_generation_settings.date_column is not None:
            date_col_name = feature_generation_settings.date_column.column_name
            frame_builder.trx_file_record_collection.sort(date_col_name)
        else:
            date_col_name = "No_Date"
        dim_col_index = 0
        for dimension_column in feature_generation_settings.dimension_columns:
            q_col_index = 0
            for quantity_column in feature_generation_settings.quantity_columns:
                watch.restart()
                target_file_name = self._get_target_file_name(reduction_settings.target_record_source,
                                                              reduction_settings.target_record_source_index)
                LogHelper.info(f"Target File: {target_file_name}, "
                               f"Date Column: {date_col_name}, "
                               f"Dimension: {dimension_column}, "
                               f"Quantity: {quantity_column}")

                frame_builder.execute(reduction_settings.num_threads, dimension_column, quantity_column,
                                      feature_generation_settings)

                df_time = watch.get_elapsed_seconds()
                LogHelper.info(f"Building Data Frame finished in {df_time} seconds")

                if partition is None:
                    partition = self._get_partition(frame_builder, algorithm_settings)

                self._add_afe_columns_to_all_afe_columns(frame_builder.name_to_column,
                                                         reduction_settings.target_record_source,
                                                         reduction_settings.target_record_source_index)
                watch.restart()

                selected_cols = self._get_selected_cols(reduction_settings.num_threads,
                                                        partition,
                                                        algorithm_settings,
                                                        frame_builder,
                                                        frame_builder.frame)
                model_time = watch.get_elapsed_seconds()
                LogHelper.info(f"Building non-interaction model finished in {model_time} seconds")

                for col in selected_cols:
                    all_columns_frame.try_add(col, frame_builder.frame.get_value(col))

                if self._settings.output_settings.enable_write_output:
                    PersistHelper.print_report(selected_cols, file, dimension_column, quantity_column,
                                               frame_builder.name_to_column,
                                               reduction_settings.trx_file_record_collection.transaction_file_stats)

                self._persist_frame_output(frame_builder,
                                           date_col_name,
                                           dimension_column, quantity_column,
                                           order, dim_col_index, q_col_index)
                LogHelper.info(f"Remaining input columns: {len(all_columns_frame.get_column_names())}")
                self.__update_exec_service(reduction_settings,
                                           order,
                                           dimension_column,
                                           frame_builder,
                                           selected_cols,
                                           df_time,
                                           model_time)
                watch.restart()
                frame_builder.clean_frame()
                LogHelper.info(f"Cleaned frame in {watch.get_elapsed_seconds(True)} seconds. ")
                LogHelper.info(f"Iteration finished for Target File: {target_file_name}, "
                               f"Dimension: {dimension_column}, "
                               f"Quantity: {quantity_column}")
                q_col_index += 1
            dim_col_index += 1
        return partition

    @abc.abstractmethod
    def _get_data_frame_builder(self, target_file_record_collection: TargetFileRecordCollection,
                                trx_file_record_collection: TransactionFileRecordCollection):
        """Return DataFrameBuilder instance"""

    @staticmethod
    def _get_partition(frame_builder: DataFrameBuilder = None,
                       algorithm_settings: AfeAlgorithmSettings = None) -> Optional[IDataPartition]:
        # pylint: disable=unused-argument
        return None

    def _get_selected_cols(self, num_threads: int,
                           partition: IDataPartition = None,
                           algorithm_settings: AfeAlgorithmSettings = None,
                           frame_builder: DataFrameBuilder = None,
                           frame_with_all_columns: DictDataFrame = None,
                           is_final=False) -> List[str]:

        raise NotImplementedError

    def _get_final_columns_metrics(self, num_threads: int, frame_builder: DataFrameBuilder,
                                   frame_with_all_columns: DictDataFrame, reduced_columns: List[str],
                                   algorithm_settings: AfeSupervisedAlgorithmSettings) -> dict:
        """
        Generate extra metrics for final selected AfeColumns
        """
        # pylint: disable=no-self-use,unused-argument
        return None

    def control_target_record_files(self, multi_target_entity_container_service: MultiTargetEntityContainerService):
        """
        control sample size and min_data_in_leaf ratio.
        :param multi_target_entity_container_service:
        :return: true or false
        """

    def __run_final_model(self, num_threads: int,
                          partition: IDataPartition,
                          frame_builder: DataFrameBuilder,
                          file,
                          trx_file_record_collection: TransactionFileRecordCollection,
                          frame_with_all_columns: DictDataFrame = None) -> Tuple[Dict[str, AfeColumn], dict]:
        watch = StopWatch(start=True)
        watch.restart()
        LogHelper.info("Building final model")
        algorithm_settings = self._settings.algorithm_settings
        selected_cols = self._get_selected_cols(num_threads,
                                                partition,
                                                algorithm_settings,
                                                frame_builder,
                                                frame_with_all_columns,
                                                is_final=True)
        # pylint: disable=assignment-from-none
        final_col_metrics = self._get_final_columns_metrics(num_threads, frame_builder, frame_with_all_columns,
                                                            selected_cols, algorithm_settings)
        reduction_extra_info = {"final_column_metrics": final_col_metrics}
        _dict: Dict[str, AfeColumn] = {}
        for col in selected_cols:
            afe_column = frame_builder.name_to_column[col]
            _dict[afe_column.column_name] = afe_column

        if self._settings.output_settings.enable_write_output:
            PersistHelper.print_report(selected_cols, file, "", "", frame_builder.name_to_column,
                                       trx_file_record_collection.transaction_file_stats)
        LogHelper.info(f"Building final model finished in {watch.get_elapsed_seconds(True)} seconds")

        return _dict, reduction_extra_info

    def _add_afe_columns_to_all_afe_columns(self, name_to_column: Dict[str, AfeColumnType],
                                            target_record_source: RecordSource,
                                            target_record_source_index: int):
        if not self._settings.output_settings.return_all_afe_columns and not \
                self._settings.output_settings.enable_all_feature_lookup_output_to_csv:
            return
        source = self._get_afe_column_source(target_record_source, target_record_source_index)
        for name, afe_column in name_to_column.items():
            if name not in self._all_afe_columns:  # pylint: disable=unsupported-membership-test
                afe_column.source = source
                # pylint: disable=unsupported-assignment-operation
                self._all_afe_columns[name] = afe_column

    def _persist_frame_output(self, frame_builder,  # pylint: disable=too-many-arguments
                              date_col_name, dimension_column, quantity_column,
                              date_col_index, dim_col_index, q_col_index):
        """Persists current frame"""

    @staticmethod
    def _persist_lookup_csv(file_prefix: str, csv_data):
        folder_root = os.path.join(FlCoreStaticObjects.get_master_output_directory(), "AfeLookupCsvOutput")
        directory_helper.create(folder_root)
        date_str = date_helper.format_date(date_helper.now(), "%Y%m%d_%H%M%S_%f")[:-3]
        lookup_file_name = f"{file_prefix}_{date_str}.csv"
        file_io_helper.write_to_file(os.path.join(folder_root, lookup_file_name), csv_data)

    def _persist_lookup_data_table(self, lookup_data_table):
        """Persist lookup data table"""
        # pylint: disable=no-self-use

    @staticmethod
    def _feature_frame_to_csv(lookup_data_frame: pd.DataFrame):
        csv_data = "FEATURE,DIMENSION,DIMENSION_SET,QUANTITY,OPERATOR,DATE_COLUMN," \
                   "TIME_WINDOW,RESOLUTION,OFFSET\n"
        for _, row in lookup_data_frame.iterrows():
            record = AfeColumnDto()
            feature = None if pd.isnull(row["FEATURE"]) else str(row["FEATURE"])
            record.name = None if pd.isnull(row["FEATURE_EXTENDED_NAME"]) else str(row["FEATURE_EXTENDED_NAME"])
            record.date_column_name = None if pd.isnull(row["DATE_COLUMN_NAME"]) else str(row["DATE_COLUMN_NAME"])
            record.dimension = None if pd.isnull(row["DIMENSION"]) else str(row["DIMENSION"])
            record.dimension_set = None if pd.isnull(row["DIMENSION_SET"]) else str(row["DIMENSION_SET"])
            record.quantity = None if pd.isnull(row["QUANTITY"]) else str(row["QUANTITY"])
            record.operator = None if pd.isnull(row["OPERATOR"]) else str(row["OPERATOR"])
            record.time_window = None if pd.isnull(row["TIME_WINDOW"]) else row["TIME_WINDOW"]
            record.time_resolution = None if pd.isnull(row["RESOLUTION"]) else str(row["RESOLUTION"])
            record.offset = None if pd.isnull(row["DATE_OFFSET"]) else row["DATE_OFFSET"]

            csv_data += ",".join([effective_value(feature), effective_value(record.dimension),
                                  effective_value(record.dimension_set), record.quantity, record.operator,
                                  effective_value(record.date_column_name),
                                  str(record.time_window),
                                  effective_value(record.time_resolution), str(record.offset)])

            csv_data += "\n"
        return csv_data

    def _read_transactions_file(self, d_columns, q_columns,
                                interval_per_entity_per_date_col: Dict[str, Dict[str, DateInterval]],
                                unique_entity_list: List[str]):
        watch = StopWatch(True)

        LogHelper.info("Started reading transactions file")

        trx_reader = trx_reader_helper.get_trx_file_record_reader_for_modelling(
            d_columns,
            q_columns,
            self._settings.data_source_settings,
            self._settings.algorithm_settings,
            interval_per_entity_per_date_col,
            unique_entity_list
        )

        trx_file_record_collection: TransactionFileRecordCollection = trx_reader.read()
        LogHelper.info(f"Finished reading transactions file in {watch.get_elapsed_seconds(True)} seconds")

        return trx_file_record_collection

    def __update_exec_service(self,
                              reduction_settings: ModellingReductionSettings,
                              order: int,
                              dimension_column: str,
                              frame_builder: DataFrameBuilder,
                              selected_cols: List[str],
                              df_time: float,
                              model_time: float):
        # pylint: disable=too-many-arguments
        if isinstance(self._exec_plan_service, BaseExecutionPlanService):
            return
        algorithm_settings: AfeSupervisedAlgorithmSettings or AfeUnsupervisedAlgorithmSettings = \
            self._settings.algorithm_settings
        if self._exec_plan_service.iteration_count == 0:
            self._exec_plan_service.calculate_calibrated_reduce_time(reduction_settings.target_record_source,
                                                                     order,
                                                                     dimension_column,
                                                                     df_time,
                                                                     model_time)
            plan = self._exec_plan_service.get_plan()  # pylint: disable=assignment-from-none
            if plan is not None:
                LogHelper.info(f'Calibrated plan is : {plan}')

        trx_collection = reduction_settings.trx_file_record_collection

        self._exec_plan_service.add_df_builder_statistic(
            reduction_settings.target_file_record_collection.sampled_count,
            trx_collection.actual_record_count,
            len(np.unique(trx_collection.d_arrays[:trx_collection.actual_record_count,
                          trx_collection.d_map[dimension_column]])),
            order, len(frame_builder.frame.get_column_names()), df_time)

        data_frame = frame_builder.frame.data_frame
        if self._settings.afe_learning_type == AfeLearningType.Supervised:
            self._exec_plan_service.add_supervised_statistic(data_frame.shape[0],
                                                             data_frame.shape[1], model_time)
        else:
            self._exec_plan_service.add_unsupervised_statistic(data_frame.shape[1],
                                                               algorithm_settings.bin_count,
                                                               data_frame.shape[0],
                                                               algorithm_settings.r_factor,
                                                               len(selected_cols),
                                                               model_time)

        self._exec_plan_service.iteration_count += 1
        LogHelper.info(f'{self._exec_plan_service.iteration_count} of '
                       f'{self._exec_plan_service.total_reduction_loop} reduction steps are completed')

    @classmethod
    def _get_afe_column_source(cls, target_record_source: RecordSource, record_source_index: int):
        target_file_name = cls._get_target_file_name(target_record_source, record_source_index)
        if target_record_source.get_type() == RecordSourceType.DATABASE:
            source = f"{target_file_name} at {target_record_source.source.connection_name}"
        else:
            source = target_file_name
        return source

    @classmethod
    def _get_target_file_name(cls, target_record_source: RecordSource, record_source_index: int):
        source_type = target_record_source.get_type()
        if source_type == RecordSourceType.TEXT:
            return target_record_source.source
        return f"Target {record_source_index}"

    @staticmethod
    def __get_report_file(output_settings, target_record_source, record_source_index):

        if target_record_source.get_type() == RecordSourceType.DATABASE:
            report_file_name = f"{output_settings.output_prefix}_{target_record_source.source.table_name}_REPORT.txt"
        else:
            report_file_name = f"{output_settings.output_prefix}_TARGET{record_source_index}_REPORT.txt"

        report_file_path = os.path.join(output_settings.output_folder, report_file_name)

        directory_helper.create(output_settings.output_folder)
        file = None
        if output_settings.enable_write_output:
            file = open(report_file_path, "w+", encoding="utf8")  # pylint: disable=consider-using-with

        return file
