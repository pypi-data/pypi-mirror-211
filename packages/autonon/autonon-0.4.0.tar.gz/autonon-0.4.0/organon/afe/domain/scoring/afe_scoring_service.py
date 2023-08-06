"""This module includes ScoringService class."""
from datetime import datetime
from typing import List, Dict, TypeVar, Generic

import numpy as np
import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.dataaccess.services.transaction_file_record_reader import TransactionFileRecordReader
from organon.afe.domain.common import afe_date_helper
from organon.afe.domain.common.afe_date_helper import get_str_to_date_converter
from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType
from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.enums.binary_target_class import BinaryTargetClass
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.modelling.businessobjects.data_frame_builder import DataFrameBuilder
from organon.afe.domain.modelling.businessobjects.multi_target_entity_container import MultiTargetEntityContainer
from organon.afe.domain.modelling.businessobjects.target_file_record import TargetFileRecord
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats
from organon.afe.domain.modelling.supervised.multi_target_entity_container_service import \
    MultiTargetEntityContainerService
from organon.afe.domain.settings.base_afe_scoring_settings import BaseAfeScoringSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import list_helper, date_helper
from organon.fl.logging.helpers.log_helper import LogHelper

AfeScoringSettingsType = TypeVar("AfeScoringSettingsType", bound=BaseAfeScoringSettings)


class AfeScoringService(Generic[AfeScoringSettingsType]):
    """Afe Scoring Service class."""

    def __init__(self, scoring_settings: AfeScoringSettingsType):
        self.scoring_settings = scoring_settings

    def score(self, num_of_threads: int = None, for_date: str or int or datetime = None):
        """Score afe using given number of threads

        :param for_date: if given, scoring will be done for given date and no target file will be used
        :param int num_of_threads: Number of threads/processes to run scoring in parallel
        """
        if num_of_threads is None:
            num_of_threads = self.scoring_settings.process_settings.number_of_cores

        return self.score_in_memory(num_of_threads, for_date=for_date)

    def score_in_memory(self, num_of_threads: int, for_date: datetime = None) -> pd.DataFrame:
        """Scores afe in-memory"""

        if for_date is not None and not isinstance(for_date, datetime):
            try:
                target_date_col = self.scoring_settings.model_output.target_descriptor.date_column
                converter = get_str_to_date_converter(target_date_col.date_column_type, target_date_col.custom_format)
                for_date = converter(str(for_date))
            except Exception as exc:
                raise KnownException("for_date was not given in target column format and type") from exc

        LogHelper.info("Scoring in-memory")

        features = list(self.scoring_settings.model_output.output_features.values())

        LogHelper.info("Started creating data structures needed prior to reading transactions file")

        d_columns = self.__update_column_list(list({feature.afe_column.dimension_name for feature in features}),
                                              AfeStaticObjects.empty_dimension_column)
        q_columns = self.__update_column_list(list({feature.afe_column.quantity_name for feature in features}),
                                              AfeStaticObjects.empty_quantity_column)

        trx_stats_from_modelling = self.scoring_settings.model_output.transaction_file_stats

        max_horizon_per_date_col = self._get_max_horizon_per_date_col()

        if for_date is None:
            multi_target_entity_container_service = self._get_multi_target_entity_container_service()
            multi_target_entity_container_service.execute()
            multi_target_entity_container = multi_target_entity_container_service.container
            target_file_record_collection = list(multi_target_entity_container.records_per_file.values())[0]
            trx_file_record_collection = self._get_transaction_file_record_collection(d_columns,
                                                                                      q_columns,
                                                                                      trx_stats_from_modelling,
                                                                                      max_horizon_per_date_col,
                                                                                      target_file_record_collection,
                                                                                      multi_target_entity_container
                                                                                      )
        else:
            trx_file_record_collection = self.__get_transaction_file_record_collection_for_score_date(
                d_columns,
                q_columns,
                trx_stats_from_modelling,
                max_horizon_per_date_col,
                for_date)
            target_file_record_collection = TargetFileRecordCollection(len(trx_file_record_collection.entity_index_map))
            for_date_int = date_helper.get_date_as_integer(for_date)
            for entity in trx_file_record_collection.entity_index_map:
                record = TargetFileRecord()
                record.entity_id = entity
                record.event_date = for_date_int
                record.target_binary = BinaryTargetClass.NAN
                target_file_record_collection.append(record)

        frame_builder = self._get_data_frame_builder(trx_file_record_collection, target_file_record_collection,
                                                     trx_stats_from_modelling)
        frame_builder.execute_for_afe_columns(num_of_threads, self.scoring_settings.model_output.output_features)
        data_frame = frame_builder.get_frame_as_pandas_dataframe()
        target_descriptor = self.scoring_settings.model_output.target_descriptor

        data_frame.rename(
            columns={
                AfeStaticObjects.distinct_entities_entity_column_name: target_descriptor.entity_column_name
            },
            inplace=True)
        if target_descriptor.date_column is not None:
            date_col_name = target_descriptor.date_column.column_name
            data_frame.rename(
                columns={
                    AfeStaticObjects.event_date_column_name: date_col_name
                },
                inplace=True)
            if target_descriptor.date_column.date_column_type != AfeDateColumnType.DateTime:
                converter_func = afe_date_helper.get_date_to_str_converter(
                    target_descriptor.date_column.date_column_type, target_descriptor.date_column.custom_format)
                data_frame[date_col_name] = data_frame[date_col_name].apply(converter_func)

        data_frame.rename(columns={col: col.upper() for col in data_frame.columns}, inplace=True)

        data_frame_new = AfeScoringService.__change_value_for_mode_operator(frame_builder,
                                                                            trx_stats_from_modelling, data_frame)

        return data_frame_new

    def _get_multi_target_entity_container_service(self):
        return MultiTargetEntityContainerService(
            [self.scoring_settings.target_record_source],
            self.scoring_settings.model_output.target_descriptor, is_scoring=True)

    def _get_data_frame_builder(self, trx_file_record_collection: TransactionFileRecordCollection,
                                target_file_record_collection: TargetFileRecordCollection,
                                transaction_file_stats: TransactionFileStats) -> DataFrameBuilder:
        frame_builder = DataFrameBuilder(self.scoring_settings.model_output.target_descriptor,
                                         target_file_record_collection,
                                         trx_file_record_collection,
                                         transaction_file_stats=transaction_file_stats,
                                         max_num_of_columns=len(self.scoring_settings.model_output.output_features))
        return frame_builder

    def _get_max_horizon_per_date_col(self) -> Dict[str, int]:
        max_horizon_per_date_col = {}
        for feature in self.scoring_settings.model_output.output_features.values():
            if feature.afe_column.date_column is not None:
                date_col = feature.afe_column.date_column
                max_time_window = feature.afe_column.time_window
                if date_col.column_name in max_horizon_per_date_col:
                    prev_max = max_horizon_per_date_col[date_col.column_name]
                    max_horizon_per_date_col[date_col.column_name] = max(prev_max, max_time_window)
                else:
                    max_horizon_per_date_col[date_col.column_name] = max_time_window
        return max_horizon_per_date_col

    @staticmethod
    def __change_value_for_mode_operator(frame_builder, trx_file_stats, data_frame):
        for column_name, afe_column in frame_builder.name_to_column.items():
            histogram = trx_file_stats.get_histogram(afe_column.dimension_name)
            if AfeOperator.Mode.name == afe_column.operator.name:
                new_column_name = frame_builder.new_col_names_map[column_name]
                data_frame[new_column_name] = data_frame[new_column_name] \
                    .apply(lambda x, h=histogram: h.reverse_index[int(x)] if not pd.isna(x) else x)
        return data_frame

    def _get_transaction_file_record_collection(self,
                                                d_columns: List[str], q_columns: List[str],
                                                trx_stats_from_modelling: TransactionFileStats,
                                                max_horizon_per_date_col: Dict[str, int],
                                                target_file_record_collection: TargetFileRecordCollection = None,
                                                multi_target_entity_container: MultiTargetEntityContainer = None):

        entity_col_name = AfeStaticObjects.distinct_entities_entity_column_name
        distinct_entity_list = np.unique(target_file_record_collection.
                                         entities[~pd.isnull(target_file_record_collection.entities)]).tolist()
        distinct_entities_df = pd.DataFrame(
            {entity_col_name: distinct_entity_list})
        distinct_entities_record_source = RecordSource(source=distinct_entities_df)
        interval_per_entity_per_date_col = {}

        date_columns = {}

        distinct_date_columns_dict = {
            feature.afe_column.date_column.column_name: (feature.afe_column.date_resolution, feature.afe_column.offset)
            for feature in self.scoring_settings.model_output.output_features.values()
            if feature.afe_column.date_column is not None}

        for date_column_name, (resolution, offset) in distinct_date_columns_dict.items():
            max_horizon = max_horizon_per_date_col[date_column_name]
            interval_per_entity = multi_target_entity_container.get_date_interval_per_entity(resolution,
                                                                                             max_horizon, offset)
            interval_per_entity_per_date_col[date_column_name] = interval_per_entity
            afe_date_col = self.scoring_settings.model_output.trx_date_columns[date_column_name]
            date_columns[date_column_name] = afe_date_col

        empty_col_interval_per_entity = multi_target_entity_container.get_date_interval_per_entity(
            DateResolution.Day, 1, 0)
        interval_per_entity_per_date_col["__NO_DATE_COL"] = empty_col_interval_per_entity

        transaction_file_reader = self._get_transaction_file_record_reader(date_columns,
                                                                           None,
                                                                           interval_per_entity_per_date_col,
                                                                           d_columns, q_columns,
                                                                           trx_stats_from_modelling,
                                                                           distinct_entities_record_source,
                                                                           entity_col_name)

        LogHelper.info("Started reading transactions file.")
        trx_file_record_collection: TransactionFileRecordCollection = transaction_file_reader.read()
        LogHelper.info("Finished reading transactions file.")

        return trx_file_record_collection

    def __get_transaction_file_record_collection_for_score_date(self,
                                                                d_columns: List[str], q_columns: List[str],
                                                                trx_stats_from_modelling: TransactionFileStats,
                                                                max_horizon_per_date_col: Dict[str, int],
                                                                score_date: datetime):
        date_columns = self.scoring_settings.model_output.trx_date_columns
        interval_per_date_col = {}
        for feature in self.scoring_settings.model_output.output_features.values():
            date_col = feature.afe_column.date_column
            if date_col is not None and date_col.column_name not in interval_per_date_col:
                max_horizon = max_horizon_per_date_col[date_col.column_name]
                func_min = afe_date_helper.get_date_subtraction_func(feature.afe_column.date_resolution,
                                                                     max_horizon + feature.afe_column.offset)
                func_max = afe_date_helper.get_date_subtraction_func(feature.afe_column.date_resolution,
                                                                     feature.afe_column.offset)
                date_as_int = date_helper.get_date_as_integer(score_date)
                min_date = date_helper.get_integer_as_date(func_min(date_as_int))
                max_date = date_helper.get_integer_as_date(func_max(date_as_int))
                interval_per_date_col[date_col.column_name] = (min_date, max_date)

        transaction_file_reader = self._get_transaction_file_record_reader(date_columns,
                                                                           interval_per_date_col,
                                                                           None,
                                                                           d_columns, q_columns,
                                                                           trx_stats_from_modelling,
                                                                           None, None)

        LogHelper.info("Started reading transactions file.")
        trx_file_record_collection: TransactionFileRecordCollection = transaction_file_reader.read()
        LogHelper.info("Finished reading transactions file.")
        return trx_file_record_collection

    def _get_transaction_file_record_reader(self, date_columns, interval_per_date_col,
                                            interval_per_entity_per_date_col,
                                            d_columns, q_columns, trx_stats_from_modelling,
                                            distinct_entities_record_source, entity_col_name
                                            ):
        # pylint: disable=too-many-arguments
        return TransactionFileRecordReader(
            self.scoring_settings.raw_input_source,
            date_columns,
            self.scoring_settings.model_output.trx_entity_column,
            interval_per_entity_per_date_column=interval_per_entity_per_date_col,
            interval_per_date_column=interval_per_date_col,
            dimension_columns=d_columns, quantity_columns=q_columns,
            distinct_entity_source=distinct_entities_record_source,
            entity_source_entity_column=entity_col_name,
            transaction_file_stats=trx_stats_from_modelling,
            reading_settings=self.scoring_settings.trx_reading_settings
        )

    @staticmethod
    def __update_column_list(base_list: List[str], new_column: str) -> List[str]:
        if list_helper.is_null_or_empty(base_list):
            return [new_column]
        if new_column not in base_list:
            base_list.append(new_column)
        return list(set(base_list))
