"""Includes SampleDataServiceHelper class."""
from datetime import datetime
from typing import Dict, Tuple, Callable

import pandas as pd

from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.afe.domain.settings.auto_column_decider_settings import AutoColumnDeciderSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.businessobjects.date_interval import DateInterval
from organon.fl.core.exceptionhandling.known_exception import KnownException


class SampleDataServiceHelper:
    """Includes common methods for sample data services."""

    def __init__(self, trx_record_source: RecordSource,
                 entity_col: str, func_per_date_column: Dict[str, Callable[[str], datetime]],
                 interval_per_entity_per_date_column: Dict[str, Dict[str, DateInterval]],
                 distinct_entity_source: RecordSource, auto_col_decider_settings: AutoColumnDeciderSettings):
        self.trx_record_source = trx_record_source
        self.__trx_entity_column = entity_col
        self.func_per_date_column = func_per_date_column
        self.interval_per_entity_per_date_column = interval_per_entity_per_date_column
        self.distinct_entity_source = distinct_entity_source
        self.auto_column_decider_settings = auto_col_decider_settings

    def read_dataframe_source(self, unique_entities_set, min_max_dates_per_date_column):
        """
        Reads pandas DataFrame source.
        :return: TransactionFileRecordCollection containing DataFrame records
        """
        if self.distinct_entity_source is not None and \
                self.distinct_entity_source.get_type() != RecordSourceType.DATA_FRAME:
            raise KnownException("Distinct entity source should be a dataframe")
        data_frame: pd.DataFrame = self.trx_record_source.source

        return self._get_reduced_frame(data_frame, min_max_dates_per_date_column, unique_entities_set)

    def read_text_source(self, unique_entities_set, min_max_dates_per_date_column, chunksize):
        """
        Reads text source.
        :return: TransactionFileRecordCollection containing text records
        """
        if self.distinct_entity_source is not None and \
                self.distinct_entity_source.get_type() != RecordSourceType.DATA_FRAME:
            raise KnownException("Distinct entity source should be a dataframe")

        record_source = self.trx_record_source
        frame_chunks = []
        for data_frame in pd.read_csv(record_source.source, sep=",", chunksize=chunksize):
            reduced_frame = self._get_reduced_frame(data_frame, min_max_dates_per_date_column, unique_entities_set)
            frame_chunks.append(
                reduced_frame.sample(
                    frac=self.auto_column_decider_settings.sampling_ratio))

        return pd.concat(frame_chunks)

    def _get_reduced_frame(self, data_frame: pd.DataFrame,
                           min_max_dates_per_date_column: Dict[str, Tuple[datetime, datetime]],
                           unique_entities_set: set = None):
        entity_ids = data_frame[self.__trx_entity_column].astype(str)
        all_conditions_series = None
        for date_col in min_max_dates_per_date_column:
            dates = data_frame[date_col].astype(str).map(self.func_per_date_column[date_col])
            min_date, max_date = min_max_dates_per_date_column[date_col]
            condition_series = (max_date >= dates) & (dates >= min_date) & \
                               entity_ids.isin(self.interval_per_entity_per_date_column[date_col])
            if all_conditions_series is None:
                all_conditions_series = condition_series
            else:
                all_conditions_series |= condition_series
        if all_conditions_series is None:
            return data_frame

        if unique_entities_set:
            all_conditions_series &= entity_ids.isin(unique_entities_set)

        return data_frame.loc[all_conditions_series]
