"""Includes RecordSourceFilterHelper class."""
from collections import abc
from typing import List

import numpy as np
import pandas as pd
from pandas.io.parsers import TextFileReader

from organon.fl.core.enums.datetime_token import DatetimeToken
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import list_helper
from organon.idq.domain.settings.abstractions.dq_base_input_source_settings import DqBaseInputSourceSettings
from organon.idq.domain.settings.date_value_definition import DateValueDefinition
from organon.idq.domain.settings.input_source.dq_file_input_source_settings import DqFileInputSourceSettings
from organon.idq.domain.settings.partition_info import PartitionInfo


class FilteredTextFileReader(abc.Iterator):
    """Iterator class for iterating csv file using TextFileReader and returning rows after filtering"""

    def __init__(self, text_file_reader: TextFileReader, settings: DqFileInputSourceSettings):
        self._text_file_reader = text_file_reader
        self._settings = settings

    def __next__(self):
        data_frame = self._text_file_reader.__next__()
        return RecordSourceFilterHelper.get_filtered_dataframe(data_frame, self._settings)


class RecordSourceFilterHelper:
    """Includes helper functions for reading a record source with filter"""

    @classmethod
    def read_csv_with_chunks(cls, settings: DqFileInputSourceSettings) -> FilteredTextFileReader:
        """Returns pandas TextFileReader object for reading with chunks according to given DqFileInputSourceSettings"""
        record_source: str = settings.source.locator
        chunk_size = settings.number_of_rows_per_step
        included_columns = settings.included_columns
        sep = settings.csv_separator
        date_columns = settings.date_columns
        if included_columns is None:
            dfs = pd.read_csv(record_source, sep=sep, chunksize=chunk_size, parse_dates=date_columns)
        else:
            dfs = pd.read_csv(record_source, sep=sep, chunksize=chunk_size, usecols=included_columns,
                              parse_dates=date_columns)
        return FilteredTextFileReader(dfs, settings)

    @classmethod
    def get_filtered_dataframe(cls, data_frame: pd.DataFrame, settings: DqBaseInputSourceSettings) -> pd.DataFrame:
        """Filters given dataframe according to given input source settings"""
        data_frame = cls._filter_by_partition(data_frame, settings.partition_info_list)
        if settings.filter_callable is not None:
            try:
                data_frame = settings.filter_callable(data_frame)
            except Exception as exc:
                raise KnownException("Error occurred while executing 'filter_callable'") from exc
            if not isinstance(data_frame, pd.DataFrame):
                raise KnownException(f"'filter_callable' is expected to return a pandas DataFrame. "
                                     f"Returned: {type(data_frame).__name__}")
        return data_frame

    @classmethod
    def _filter_by_partition(cls, data_frame: pd.DataFrame, partition_info_list: List[PartitionInfo]) -> pd.DataFrame:
        """Filters given dataframe according to given partition info"""
        if list_helper.is_null_or_empty(partition_info_list):
            return data_frame
        all_filter = cls.__get_filter(data_frame, partition_info_list)
        return data_frame[all_filter]

    @classmethod
    def __get_filter(cls, data_frame: pd.DataFrame, partition_info_list: List[PartitionInfo]) -> np.array:
        """Returns df filter as pd.Series according to given partition info"""
        all_filter = np.array([True for _ in range(len(data_frame))])
        for partition_info in partition_info_list:
            is_null_filter = None
            if None in partition_info.column_values:
                is_null_filter = data_frame[partition_info.column_name].isnull().to_numpy()

            non_null_column_values = [value for value in partition_info.column_values if value is not None]

            _filter = cls.__get_filter_for_partition(data_frame, partition_info.column_name,
                                                     non_null_column_values)
            if is_null_filter is not None:
                _filter |= is_null_filter
            all_filter &= _filter
        return all_filter

    @classmethod
    def __get_filter_for_partition(cls, data_frame: pd.DataFrame, column_name: str,
                                   non_null_column_values: list) -> np.array:
        if len(non_null_column_values) == 0:
            return np.array([True for _ in range(len(data_frame))])
        first_val = non_null_column_values[0]
        if isinstance(first_val, DateValueDefinition):
            format_val_dict = {}
            for val in non_null_column_values:
                conversion_format = cls.__get_str_conversion_format(val.get_datetime_tokens())
                val_str = cls._get_column_value_string_for_date_column(val)
                if conversion_format in format_val_dict:
                    format_val_dict[conversion_format].append(val_str)
                else:
                    format_val_dict[conversion_format] = [val_str]
            date_filter = np.array([False for _ in range(len(data_frame))])
            for conversion_format, value_strings in format_val_dict.items():
                date_filter |= data_frame[column_name].dt.strftime(conversion_format).isin(value_strings).to_numpy()
            return date_filter
        return data_frame[column_name].isin(non_null_column_values).to_numpy()

    @classmethod
    def _get_column_value_string_for_date_column(cls, column_value: DateValueDefinition):
        date_str = ""
        if column_value.year is not None:
            date_str += ("000" + str(column_value.year))[-4:]
        if column_value.month is not None:
            date_str += ("0" + str(column_value.month))[-2:]
        if column_value.day is not None:
            date_str += ("0" + str(column_value.day))[-2:]
        if column_value.hour is not None:
            date_str += ("0" + str(column_value.hour))[-2:]
        return date_str

    @classmethod
    def __get_str_conversion_format(cls, datetime_tokens: List[DatetimeToken]) -> str:
        conversion_str = ""
        if DatetimeToken.YEAR in datetime_tokens:
            conversion_str += "%Y"
        if DatetimeToken.MONTH in datetime_tokens:
            conversion_str += "%m"
        if DatetimeToken.DAY in datetime_tokens:
            conversion_str += "%d"
        if DatetimeToken.HOUR in datetime_tokens:
            conversion_str += "%H"
        return conversion_str
