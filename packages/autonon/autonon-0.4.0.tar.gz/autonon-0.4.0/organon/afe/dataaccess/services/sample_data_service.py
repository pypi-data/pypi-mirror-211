"""
This module includes SampleDataService for getting a sample data frame
"""

from datetime import datetime
from typing import Dict, Tuple

import pandas as pd

from organon.afe.dataaccess.services.i_sample_data_service import ISampleDataService
from organon.afe.dataaccess.services.sample_data_service_helper import SampleDataServiceHelper
from organon.afe.dataaccess.services.transaction_file_record_reader import TransactionFileRecordReader
from organon.afe.domain.settings.afe_algorithm_settings import AfeAlgorithmSettings
from organon.afe.domain.settings.base_afe_data_settings import BaseAfeDataSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.businessobjects.date_interval import DateInterval


class SampleDataService(TransactionFileRecordReader, ISampleDataService):
    """
    This class handles getting sample data frame from different sources such as Database, dataframe, csv file.
    """

    def __init__(self, data_source_settings: BaseAfeDataSettings,
                 algorithm_settings: AfeAlgorithmSettings,
                 distinct_entity_source: RecordSource = None,
                 entity_source_entity_column: str = None,
                 interval_per_entity_per_date_column: Dict[str, Dict[str, DateInterval]] = None,
                 min_date: datetime = None,
                 max_date: datetime = None):
        # pylint: disable=too-many-arguments
        descriptor = data_source_settings.trx_descriptor
        trx_record_source = descriptor.modelling_raw_input_source

        date_col = descriptor.feature_gen_setting.date_column
        date_columns, min_max_dates_per_date_column = {}, {}
        if date_col is not None:
            date_columns = {date_col.column_name: date_col}
            if descriptor.feature_gen_setting.max_observation_date is not None:
                min_max_dates_per_date_column = {date_col.column_name:
                                                     (None, descriptor.feature_gen_setting.max_observation_date)}

        super().__init__(
            trx_record_source,
            date_columns,
            descriptor.entity_column_name,
            interval_per_entity_per_date_column=interval_per_entity_per_date_column,
            distinct_entity_source=distinct_entity_source,
            entity_source_entity_column=entity_source_entity_column,
            min_max_dates_per_date_column=min_max_dates_per_date_column,
            max_number_of_transaction_samples=data_source_settings.max_number_of_transaction_samples,
            dimension_compression_ratio=algorithm_settings.dimension_compression_ratio,
            dimension_max_cardinality=algorithm_settings.dimension_max_cardinality,
            reading_settings=data_source_settings.trx_descriptor.reading_settings
        )
        self.data_source_settings = data_source_settings
        self.__trx_entity_column: str = descriptor.entity_column_name
        self.__min_date = min_date
        self.__max_date = max_date
        self.helper = SampleDataServiceHelper(trx_record_source, self.__trx_entity_column,
                                              self.func_per_date_column, self.interval_per_entity_per_date_column,
                                              self.distinct_entity_source,
                                              self.data_source_settings.auto_column_decider_settings)

    def get_sample(self) -> pd.DataFrame:
        return self.read()

    def read_db_source(self):
        """
        Reads database source and creates a transaction record collection.
        :return: transaction record collection
        """
        raise NotImplementedError

    def read_dataframe_source(self):
        """
        Reads pandas DataFrame source.
        :return: TransactionFileRecordCollection containing DataFrame records
        """
        min_max_dates_per_date_column = self._get_intervals_per_date_column()
        unique_entities_set = None
        if self.distinct_entity_source is not None:
            unique_entities_set = self._get_unique_entities_set()

        return self.helper.read_dataframe_source(unique_entities_set, min_max_dates_per_date_column)

    def read_text_source(self):
        """
        Reads text source.
        :return: TransactionFileRecordCollection containing text records
        """
        min_max_dates_per_date_column = self._get_intervals_per_date_column()
        chunksize = self.data_source_settings.trx_descriptor.reading_settings \
            .number_of_rows_per_step
        unique_entities_set: set = None
        if self.distinct_entity_source is not None:
            unique_entities_set = self._get_unique_entities_set()
        return self.helper.read_text_source(unique_entities_set, min_max_dates_per_date_column, chunksize)

    def _get_intervals_per_date_column(self) -> Dict[str, Tuple[datetime, datetime]]:
        if self.__min_date is not None and self.__max_date is not None:
            if self.data_source_settings.trx_descriptor.feature_gen_setting.date_column is not None:

                return {self.data_source_settings.trx_descriptor.feature_gen_setting
                        .date_column.column_name: (self.__min_date,
                                                   self.__max_date)}
            return {}
        return super()._get_intervals_per_date_column()
