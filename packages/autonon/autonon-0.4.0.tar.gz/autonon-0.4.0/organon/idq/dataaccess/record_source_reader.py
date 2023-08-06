"""Includes RecordSourceReader class."""
from typing import Tuple

import numpy as np
import pandas as pd

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.idq.dataaccess.helpers.record_source_filter_helper import RecordSourceFilterHelper, FilteredTextFileReader
from organon.idq.domain.businessobjects.dq_data_source import DqDataSource
from organon.idq.domain.enums.dq_record_source_type import DqRecordSourceType
from organon.idq.domain.settings.abstractions.dq_base_input_source_settings import DqBaseInputSourceSettings
from organon.idq.domain.settings.input_source.dq_df_input_source_settings import DqDfInputSourceSettings
from organon.idq.domain.settings.input_source.dq_file_input_source_settings import DqFileInputSourceSettings


class RecordSourceReader:
    """
    Source reader class implementation for csv files, data frames, and db sources.
    """

    def __init__(self, data_source_settings: DqBaseInputSourceSettings, row_count: int = None):
        self.data_source_settings = data_source_settings
        self.row_count = row_count

    def read(self) -> DqDataSource:
        """
        Reads the table of records and returns a collection
        :return: A collection containing records in record source
        """
        source_type = self.data_source_settings.source.get_type()
        if source_type == DqRecordSourceType.TEXT:
            return self.read_text_source()
        if source_type == DqRecordSourceType.DATA_FRAME:
            return self.read_dataframe_source()
        raise KnownException("Record source type is not valid!")

    def read_text_source(self) -> DqDataSource:
        """
        Reads text source and returns a dq data source
        """
        if not isinstance(self.data_source_settings, DqFileInputSourceSettings):
            raise ValueError('Data source settings should be of type DqFileInputSourceSettings.')

        record_source: str = self.data_source_settings.source.locator
        included_columns = self.data_source_settings.included_columns  # included columns
        max_sample_size = self.data_source_settings.max_num_of_samples
        sep = self.data_source_settings.csv_separator
        columns = pd.read_csv(record_source, header=None, sep=sep, nrows=1).iloc[0].tolist()
        self._validate_source(included_columns, columns)

        dfs = RecordSourceFilterHelper.read_csv_with_chunks(self.data_source_settings)
        frame_chunks, full_row_count = self.read_df_chunks(dfs, max_sample_size)

        data_frame = pd.concat(frame_chunks)
        data_frame.reset_index(inplace=True, drop=True)
        data_frame = data_frame.convert_dtypes()
        dq_source = DqDataSource()
        dq_source.sampled_data = data_frame
        dq_source.full_data_row_count = full_row_count
        return dq_source

    def read_dataframe_source(self) -> DqDataSource:
        """Reads DataFrame source and returns a collection"""
        if not isinstance(self.data_source_settings, DqDfInputSourceSettings):
            raise ValueError('Data source settings should be of type DqDfInputSourceSettings.')

        ratio = self.data_source_settings.sampling_ratio
        max_sample_size = self.data_source_settings.max_num_of_samples
        source: pd.DataFrame = RecordSourceFilterHelper.get_filtered_dataframe(self.data_source_settings.source.locator,
                                                                               self.data_source_settings)
        full_row_count = len(source)
        included_columns: list = self.data_source_settings.included_columns

        self._validate_source(included_columns, list(source.columns))
        source_size = self.row_count if self.row_count is not None else len(source)
        if max_sample_size is not None and max_sample_size < source_size * ratio:
            if included_columns is None:
                data_frame: pd.DataFrame = source.sample(n=max_sample_size, replace=True,
                                                         random_state=1)
            else:
                data_frame: pd.DataFrame = source[included_columns].sample(n=max_sample_size, replace=True,
                                                                           random_state=1)
        elif ratio == 1.0:
            data_frame = source if included_columns is None else source[included_columns]
        else:
            if included_columns is None:
                data_frame: pd.DataFrame = source.sample(frac=ratio, replace=True, random_state=1)
            else:
                data_frame: pd.DataFrame = source[included_columns].sample(frac=ratio, replace=True, random_state=1)

        data_frame.reset_index(inplace=True, drop=True)

        dq_source = DqDataSource()
        dq_source.sampled_data = data_frame
        dq_source.full_data_row_count = full_row_count
        return dq_source

    def read_df_chunks(self, dfs: FilteredTextFileReader, max_sample_size: int) -> Tuple[list, int]:
        """

        :param self:
        :param dfs:
        :param max_sample_size:
        :return:
        """
        frame_chunks: list = []
        sample_count: int = 0
        is_full: bool = False
        full_row_count = 0
        for filtered_df in dfs:
            full_row_count += len(filtered_df)
            sample = filtered_df.sample(frac=self.data_source_settings.sampling_ratio)
            sample_size = len(sample)
            if sample_size + sample_count > max_sample_size:
                to_read = sample_size + sample_count - max_sample_size
                add_indices = np.random.choice(sample.index, to_read, replace=False)
                sample = sample[sample.index.isin(add_indices)]
                is_full = True
            frame_chunks.append(sample)
            sample_count += len(sample)
            if is_full:
                break

        return frame_chunks, full_row_count

    @staticmethod
    def _validate_source(included_columns: list, df_cols: list):
        """
        throws exception if source has duplicated columns
        or included_columns is not a subset of df_cols.
        :param included_columns: columns that we want to use
        :param df_cols: source columns
        :return:
        """
        RecordSourceReader.__check_included_cols(included_columns, df_cols)
        RecordSourceReader.__check_duplicated_cols(df_cols)

    @staticmethod
    def __check_included_cols(included_columns: list, df_cols: list):
        """
        throws exception if included_columns is not a subset of df_cols.
        :param included_columns: columns that we want to use
        :param df_cols: source columns
        :return:
        """
        if included_columns is not None:
            column_diff = set(included_columns) - set(df_cols)
            if len(column_diff) > 0:
                col_message_str = ""
                for col in column_diff:
                    col_message_str += col + ", "
                col_message_str = col_message_str[:-2]
                raise ValueError(f'These columns do not belong to the source: {col_message_str}.')

    @staticmethod
    def __check_duplicated_cols(df_cols: list):
        """
        throws exception if there are duplicated columns in df_cols.
        :param df_cols: source columns
        :return:
        """
        seen = set()
        dupes = [x for x in list(df_cols) if x in seen or seen.add(x)]
        if len(dupes) > 0:
            col_message_str = ""
            for dup_column in dupes:
                col_message_str += dup_column + ", "
            col_message_str = col_message_str[:-2]
            raise ValueError(f'These columns are duplicated in the source: {col_message_str}.')
