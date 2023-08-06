"""
This module includes TransactionFileRecordReader class.
"""
from datetime import datetime
from typing import Dict, Callable, Tuple, List, Optional

import numpy as np
import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.dataaccess.helpers.record_source_helper import validate_entity_column
from organon.afe.dataaccess.services.base_record_reader import BaseRecordReader
from organon.afe.domain.common import afe_date_helper
from organon.afe.domain.enums.record_source_type import RecordSourceType
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.afe_reading_settings import AfeDataReadingSettings
from organon.afe.domain.settings.record_source import RecordSource
from organon.fl.core.businessobjects.date_interval import DateInterval
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import date_helper


class TransactionFileRecordReader(BaseRecordReader):
    # pylint: disable=too-many-instance-attributes
    """
    Reads a transaction file source and creates a TransactionRecordCollection
    """
    UNKNOWN_DIMENSION_VALUE = -2

    def __init__(self,
                 trx_record_source: RecordSource,
                 date_columns: Dict[str, AfeDateColumn],
                 trx_entity_column: str,
                 dimension_columns: List[str] = None,
                 quantity_columns: List[str] = None,
                 **kwargs):
        super().__init__(trx_record_source)
        self._date_columns: Dict[str, AfeDateColumn] = date_columns
        self._trx_entity_column: str = trx_entity_column
        self._trx_record_source = trx_record_source
        self._distinct_entity_source: RecordSource = kwargs.get("distinct_entity_source")
        self._entity_source_entity_column: str = kwargs.get("entity_source_entity_column")
        self._date_col_map: Dict[str, int] = self._create_map(list(date_columns.keys()))

        self._interval_per_entity_per_date_column: Dict[str, Dict[str, DateInterval]] = \
            kwargs.get("interval_per_entity_per_date_column")

        self._interval_per_date_column: Dict[str, Tuple[datetime, datetime]] = kwargs.get("interval_per_date_column")

        if self._interval_per_date_column is not None and self._interval_per_entity_per_date_column is not None:
            raise ValueError("Please give either interval_per_date_column or interval_per_entity_per_date_column")

        self._min_max_dates_per_date_column: Dict[str, Tuple[datetime, datetime]] = \
            kwargs.get("min_max_dates_per_date_column")

        self._max_number_of_transaction_samples: int = kwargs.get("max_number_of_transaction_samples",
                                                                  np.iinfo(np.int64).max)

        self._reading_settings: AfeDataReadingSettings = kwargs.get("reading_settings",
                                                                    AfeDataReadingSettings(
                                                                        number_of_rows_per_step=100000))

        self._dimension_compression_ratio: float = kwargs.get("dimension_compression_ratio", 1.0)
        self._dimension_max_cardinality: int = kwargs.get("dimension_max_cardinality", 200)

        self._trx_file_stats: TransactionFileStats = kwargs.get("transaction_file_stats")

        self._func_per_date_column = TransactionFileRecordReader.__get_func_per_date_col_map(date_columns)

        if dimension_columns:
            self._d_map: Dict[str, int] = self._create_map(dimension_columns)
            self._non_empty_d_cols: List[str] = [elem for elem in self._d_map if
                                                 elem != AfeStaticObjects.empty_dimension_column]
        if quantity_columns:
            self._q_map: Dict[str, int] = self._create_map(quantity_columns)
            self._non_empty_q_cols: List[str] = [elem for elem in self._q_map if
                                                 elem != AfeStaticObjects.empty_quantity_column]

    @property
    def trx_record_source(self) -> RecordSource:
        """Return value of private attribute '__trx_record_source'"""
        return self._trx_record_source

    @property
    def distinct_entity_source(self) -> RecordSource:
        """Return value of private attribute '__distinct_entity_source'"""
        return self._distinct_entity_source

    @property
    def entity_source_entity_column(self) -> str:
        """Return value of private attribute '__entity_source_entity_column'"""
        return self._entity_source_entity_column

    @property
    def interval_per_entity_per_date_column(self) -> Dict[str, Dict[str, DateInterval]]:
        """Return value of private attribute '__interval_per_entity'"""
        return self._interval_per_entity_per_date_column

    @property
    def date_col_map(self) -> Dict[str, int]:
        """Return value of private attribute '__date_col_map'"""
        return self._date_col_map

    @property
    def d_map(self) -> Dict[str, int]:
        """Return value of private attribute '__d_map'"""
        return self._d_map

    @property
    def q_map(self) -> Dict[str, int]:
        """Return value of private attribute '__q_map'"""
        return self._q_map

    @property
    def func_per_date_column(self) -> Dict[str, Callable[[str], datetime]]:
        """Return value of private attribute '__func'"""
        return self._func_per_date_column

    @staticmethod
    def __get_func_per_date_col_map(date_columns: Dict[str, AfeDateColumn]):
        func_per_date_column = {}
        for date_column in date_columns.values():
            func = afe_date_helper.get_str_to_date_converter(date_column.date_column_type,
                                                             date_column.custom_format)
            func_per_date_column[date_column.column_name] = func
        return func_per_date_column

    def __get_date_interval_for_all_entities(self) -> Dict[str, Tuple[datetime, datetime]]:
        """
        Finds overall minimum and maximum dates from date boundaries of all entities
        :return: tuple containing min_date and max_date
        """
        date_interval_per_date_column = {}

        for date_column in self._date_columns.values():
            if date_column is not None:
                date_col_name = date_column.column_name
                min_date_ts: int = np.iinfo(np.int64).max
                max_date_ts: int = np.iinfo(np.int64).min
                # pylint: disable=unsubscriptable-object
                interval_per_entity = self._interval_per_entity_per_date_column[date_col_name]
                for item in interval_per_entity:
                    target_interval: DateInterval = interval_per_entity[item]
                    if target_interval.lower_bound < min_date_ts:
                        min_date_ts = target_interval.lower_bound
                    if target_interval.upper_bound > max_date_ts:
                        max_date_ts = target_interval.upper_bound
                min_date = date_helper.get_integer_as_date(min_date_ts)
                max_date = date_helper.get_integer_as_date(max_date_ts)
                date_interval_per_date_column[date_col_name] = (min_date, max_date)
        return date_interval_per_date_column

    def read_db_source(self) -> TransactionFileRecordCollection:
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
        if self._distinct_entity_source is not None and \
                self._distinct_entity_source.get_type() != RecordSourceType.DATA_FRAME:
            raise KnownException("Distinct entity source should be a dataframe")
        data_frame: pd.DataFrame = self._trx_record_source.source
        collection = self._initialize_collection(len(data_frame))
        unique_entities_set = None
        if self.distinct_entity_source is not None:
            unique_entities_set = self._get_unique_entities_set()
        self.__get_records_from_dataframe(data_frame, collection,
                                          self._max_number_of_transaction_samples,
                                          unique_entities_set)

        if self._trx_file_stats is None:
            self._collection_stats_build_indices(collection)
        collection.convert_entity_index_lists_to_array()
        return collection

    def read_text_source(self):
        """
        Reads text source.
        :return: TransactionFileRecordCollection containing text records
        """
        if self._distinct_entity_source is not None and \
                self._distinct_entity_source.get_type() != RecordSourceType.DATA_FRAME:
            raise KnownException("Distinct entity source should be a dataframe")

        created_records_num = 0
        chunksize = self._reading_settings.number_of_rows_per_step
        record_source = self._trx_record_source
        max_trx_samples = self._max_number_of_transaction_samples

        with open(record_source.source, "r", encoding="utf8") as file:
            row_count = sum(1 for row in file if row.strip() != "") - 1  # subtract for header line

        record_count = min(max_trx_samples, row_count)
        collection = self._initialize_collection(record_count)
        unique_entities_set: set = None
        if self.distinct_entity_source is not None:
            unique_entities_set = self._get_unique_entities_set()
        with open(record_source.source, encoding="utf-8") as source_file:
            for data_frame in pd.read_csv(source_file, sep=",", chunksize=chunksize):
                records_needed = max_trx_samples - created_records_num
                chunk_records_num = self.__get_records_from_dataframe(data_frame, collection,
                                                                      min(records_needed, chunksize),
                                                                      unique_entities_set)
                created_records_num += chunk_records_num
                if created_records_num >= max_trx_samples:
                    break

        if self._trx_file_stats is None:
            self._collection_stats_build_indices(collection)
        collection.convert_entity_index_lists_to_array()
        return collection

    def __get_records_from_dataframe(self, data_frame: pd.DataFrame, collection: TransactionFileRecordCollection,
                                     max_record_num: int,
                                     unique_entities_set: set = None):
        """
        Inserts records into given collection by reading the DataFrame

        :param set unique_entities_set: Set of unique entities to be read
        :param max_record_num: Maximum number of records to be created
        :param pd.DataFrame data_frame: DataFrame to be read
        :param TransactionFileRecordCollection collection: Collection to store records
        """
        trx_entity_column: str = self._trx_entity_column
        validate_entity_column("transaction", data_frame, trx_entity_column)
        trx_date_columns = [date_column.column_name for date_column in self._date_columns.values()]

        columns_ordered = [trx_entity_column]
        if len(trx_date_columns) > 0:
            columns_ordered.extend(trx_date_columns)

        columns_ordered.extend(self._non_empty_q_cols)
        columns_ordered.extend(self._non_empty_d_cols)
        column_index_map = {column: columns_ordered.index(column) for column in columns_ordered}
        created_records_num = 0

        for row_iter in data_frame.iterrows():
            frame_row = row_iter[1]
            entity_id = str(TransactionFileRecordReader.__get_col_value_from_row(frame_row, trx_entity_column))
            if unique_entities_set is not None and entity_id not in unique_entities_set:
                continue
            row = [entity_id]

            add_to_collection = True
            for date_col in trx_date_columns:
                date_value = self.func_per_date_column[date_col](str(
                    TransactionFileRecordReader.__get_col_value_from_row(frame_row, date_col)))
                row.append(date_value)
                if not self.__check_add_to_collection(date_col, date_value):
                    add_to_collection = False
                    break

            if add_to_collection:
                self.__append_column_ordered_d_and_q_column(row, frame_row)
                record_created = self.get_record_from_row(collection, row, column_index_map, convert_dates=False)
                if record_created:
                    created_records_num += 1
                    if created_records_num >= max_record_num:
                        break
        return created_records_num

    @staticmethod
    def __get_col_value_from_row(row, column_name: str):
        try:
            return row[column_name]
        except KeyError as key_err:
            raise KnownException(f"Column {key_err.args[0]} could not be found in transaction data source") from key_err

    def __check_add_to_collection(self, date_col: str, date_val: datetime):
        """Checks if row should be add to record collection"""
        min_max_dates_per_date_column = self._min_max_dates_per_date_column
        if min_max_dates_per_date_column is None or date_col not in min_max_dates_per_date_column:
            return True
        min_date, max_date = min_max_dates_per_date_column[date_col]
        if min_date is not None and date_val < min_date:
            return False
        if max_date is not None and date_val > max_date:
            return False

        return True

    def __append_column_ordered_d_and_q_column(self, row, frame_row):
        for col in self._non_empty_q_cols:
            row.append(str(TransactionFileRecordReader.__get_col_value_from_row(frame_row, col)))
        for col in self._non_empty_d_cols:
            col_value = TransactionFileRecordReader.__get_col_value_from_row(frame_row, col)
            if col_value is None:
                row.append(col_value)
            else:
                row.append(str(col_value))

    def get_record_from_row(self, collection: TransactionFileRecordCollection, row, column_positions: Dict[str, int],
                            convert_dates: bool = True):
        """
        Creates a TransactionFileRecord given a row of values
        :param convert_dates: Should be given false if date column values are already datetime objects
        :param collection: Collection instance to be filled
        :param row: A subscriptable storing entity id, date , quantity values, dimension values
        :param column_positions: Dictionary for column_name-row_index mapping
        :return: True if record was created successfully
        """
        entity_id = str(row[0])
        add_to_collection, trx_dates = self.__check_and_get_date_values(row, entity_id, column_positions, convert_dates)

        if not add_to_collection:
            return False

        q_array: List[None or int] = [None] * len(self._q_map)
        default_q_index = self._q_map[AfeStaticObjects.empty_quantity_column]
        q_array[default_q_index] = 1.0
        self.__set_q_array(column_positions, q_array, row)

        d_array = [0] * len(self._d_map)
        default_d_column: str = AfeStaticObjects.empty_dimension_column

        default_d_index = self._d_map[AfeStaticObjects.empty_dimension_column]
        d_array[default_d_index] = 0

        self.__set_d_array(column_positions, d_array, row, collection, default_d_column)

        collection.append(entity_id, trx_dates, q_array, d_array)
        return True

    def __set_q_array(self, column_positions, q_array, row):
        for q_column in self._non_empty_q_cols:
            pos: int = column_positions[q_column]
            value = row[pos]
            if value is None:
                continue
            index: int = self._q_map[q_column]
            q_array[index] = value

    def __set_d_array(self, column_positions, d_array, row, collection, default_d_column):
        if self._trx_file_stats is None:
            collection.transaction_file_stats.increment(default_d_column, "")
            for d_column in self._non_empty_d_cols:
                pos = column_positions[d_column]
                index: int = self._d_map[d_column]
                d_val = row[pos]
                if d_val is not None:
                    d_val: str = str(row[pos])
                collection.transaction_file_stats.increment(d_column, d_val)
                d_array[index] = collection.transaction_file_stats.get_index(d_column, d_val)

        else:
            for d_column in self._non_empty_d_cols:
                pos = column_positions[d_column]
                index: int = self._d_map[d_column]
                d_val = row[pos]
                if d_val is not None:
                    d_val: str = str(row[pos])
                try:
                    d_array[index] = self._trx_file_stats.get_index(d_column, d_val)
                except KeyError:
                    d_array[index] = self.UNKNOWN_DIMENSION_VALUE

    def __check_and_get_date_values(self, row, entity_id, column_positions, convert_dates):
        if len(self._date_columns) == 0:
            return True, []
        trx_dates: List[None or int] = [None] * len(self._date_col_map)
        date_cond = False

        for date_column in self._date_columns.values():
            pos: int = column_positions[date_column.column_name]
            date_val = self._func_per_date_column[date_column.column_name](str(row[pos])) \
                if convert_dates else row[pos]
            value = date_helper.get_date_as_integer(date_val)
            if value is None:
                continue
            index: int = self._date_col_map[date_column.column_name]

            if self._interval_per_date_column is not None:
                interval = self._interval_per_date_column[date_column.column_name]
                lower, upper = interval[0], interval[1]
                lower_bound_ok = True
                if lower is not None and date_val < lower:
                    lower_bound_ok = False
                upper_bound_ok = True
                if upper is not None and date_val > upper:
                    upper_bound_ok = False
                if lower_bound_ok and upper_bound_ok:
                    date_cond = True

            elif self._interval_per_entity_per_date_column is not None:
                # pylint: disable=unsubscriptable-object
                interval_per_entity = self._interval_per_entity_per_date_column[date_column.column_name]
                if entity_id in interval_per_entity:
                    if not date_cond and interval_per_entity[entity_id].contains(value):
                        date_cond = True
            else:
                date_cond = True
            trx_dates[index] = value

        return date_cond, trx_dates

    def _initialize_collection(self, record_count: int):
        """Creates and initializes a TransactionFileRecordCollection"""
        collection = TransactionFileRecordCollection(self._date_col_map,
                                                     self.d_map,
                                                     self.q_map,
                                                     record_count)
        default_d_column: str = AfeStaticObjects.empty_dimension_column
        if self._trx_file_stats is None:
            stats: TransactionFileStats = TransactionFileStats()
            stats.add(default_d_column)
            for dimension_column in self._non_empty_d_cols:
                stats.add(dimension_column)
            collection.transaction_file_stats = stats
        return collection

    def _get_intervals_per_date_column(self) -> Optional[Dict[str, Tuple[datetime, datetime]]]:
        """Returns minimum and maximum dates of concern for transaction"""
        if self._interval_per_date_column is None and self._interval_per_entity_per_date_column is None:
            return {}

        if self._interval_per_date_column is not None:
            interval_per_date_col = self._interval_per_date_column
        else:
            interval_per_date_col = self.__get_date_interval_for_all_entities()

        min_max_dates_per_date_column = {}

        for date_column in self._date_columns.values():
            if date_column is not None:
                date_col_name = date_column.column_name
                date_interval = interval_per_date_col[date_col_name]
                max_date: datetime = date_interval[1]
                min_date: datetime = date_interval[0]

                # pylint: disable=unsupported-membership-test,unsubscriptable-object
                if self._min_max_dates_per_date_column is not None and \
                        date_col_name in self._min_max_dates_per_date_column:
                    exp_min_date, exp_max_date = self._min_max_dates_per_date_column[date_col_name]

                    if exp_max_date is not None and exp_max_date < max_date:
                        max_date = exp_max_date
                    if exp_min_date is not None and min_date < exp_min_date:
                        min_date = exp_min_date

                min_max_dates_per_date_column[date_col_name] = (min_date, max_date)
        return min_max_dates_per_date_column

    def _collection_stats_build_indices(self, collection: TransactionFileRecordCollection):
        """builds indices for a trx file"""
        if collection.actual_record_count == 0:
            raise KnownException("There are no eligible records in collection")
        collection.transaction_file_stats.build_indices(
            self._dimension_compression_ratio,
            self._dimension_max_cardinality)

    def _get_unique_entities_set(self):
        return set(self._distinct_entity_source.source[self._entity_source_entity_column])

    @staticmethod
    def _create_map(column_list: List[str]) -> Dict[str, int]:
        _dict = {}
        index = 0
        for column in column_list:
            _dict[column] = index
            index += 1
        return _dict
