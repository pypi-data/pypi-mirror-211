"""
This module includes TargetFileRecordRepository class.
"""
import math
from datetime import datetime
from typing import Callable, List, Optional

import numpy as np
import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.dataaccess.helpers.record_source_helper import validate_entity_column
from organon.afe.dataaccess.services.base_record_reader import BaseRecordReader
from organon.afe.domain.common import afe_date_helper
from organon.afe.domain.enums.afe_date_column_type import AfeDateColumnType
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.enums.binary_target_class import BinaryTargetClass
from organon.afe.domain.modelling.businessobjects.target_file_record import TargetFileRecord
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.settings.record_source import RecordSource
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import date_helper
from organon.fl.core.helpers.string_helper import is_null_or_empty


class TargetFileRecordRepository(BaseRecordReader):
    """
    This class is used to create a TargetFileRecordCollection, given a TargetFileDescriptor and record source.
    """

    def __init__(self, record_source: RecordSource, file_descriptor: TargetDescriptor,
                 rejected_target_classes: List[str] = None, is_scoring=False):
        super().__init__(record_source)
        if rejected_target_classes is None:
            rejected_target_classes = []
        self._record_source: RecordSource = record_source
        self._file_descriptor: TargetDescriptor = file_descriptor
        self._rejected_target_classes = rejected_target_classes
        self._is_scoring = is_scoring
        data_column_type: AfeDateColumnType = AfeDateColumnType.DateTime
        custom_format = None
        if self._file_descriptor.date_column is not None:
            data_column_type: AfeDateColumnType = self._file_descriptor.date_column.date_column_type
            custom_format: str = self._file_descriptor.date_column.custom_format
        self._func: Callable[[str], datetime] = \
            afe_date_helper.get_str_to_date_converter(data_column_type, custom_format)

    def read_text_source(self) -> TargetFileRecordCollection:
        """
        Reads text source.

        :return: TargetFileRecordCollection containing text records
        """
        with open(self._record_source.source, "r", encoding="utf8") as file:
            row_count = sum(1 for row in file if row.strip() != "") - 1  # subtract for header line

        collection = TargetFileRecordCollection(row_count)
        chunksize = self._file_descriptor.reading_settings.number_of_rows_per_step
        initial_index = 0
        for data_frame in pd.read_csv(self._record_source.source, sep=",", chunksize=chunksize):
            self.__get_records_from_dataframe(collection, data_frame, initial_index)  # pylint: disable=(no-member)
            initial_index += len(data_frame)
        return collection

    def read_dataframe_source(self) -> TargetFileRecordCollection:
        """
        Reads pandas DataFrame source.
        :return: TargetFileRecordCollection containing pandas DataFrame records
        """
        data_frame: pd.DataFrame = self._record_source.source
        collection = TargetFileRecordCollection(len(data_frame))
        return self.__get_records_from_dataframe(collection, data_frame)

    def read_db_source(self) -> TargetFileRecordCollection:
        raise NotImplementedError

    def __get_records_from_dataframe(self, collection: TargetFileRecordCollection, data_frame: pd.DataFrame,
                                     initial_index=0):
        """
        Creates TargetFileRecords from a pandas DataFrame and stores in collection.

        :param TargetFileRecordCollection collection:
        :param pd.DataFrame data_frame:
        :param int initial_index: collection index to start adding data_frame rows
        """
        index = initial_index
        validate_entity_column("target", data_frame, self._file_descriptor.entity_column_name)
        try:
            for row_iter in data_frame.iterrows():
                frame_row = row_iter[1]
                entity_id = frame_row[self._file_descriptor.entity_column_name]
                target = None
                if self._is_scoring:
                    if self._file_descriptor.target_column is not None and \
                            self._file_descriptor.target_column.column_name in frame_row:
                        target = frame_row[self._file_descriptor.target_column.column_name]
                else:
                    if self._file_descriptor.target_column is not None:
                        target = frame_row[self._file_descriptor.target_column.column_name]
                if entity_id is None or (isinstance(entity_id, float) and math.isnan(entity_id)):
                    continue
                if self._file_descriptor.date_column is not None:
                    date_value = frame_row[self._file_descriptor.date_column.column_name]
                    if date_value is None or (isinstance(date_value, float) and math.isnan(date_value)):
                        continue
                    record = self._get_record_from_row([entity_id, date_value, target])
                else:
                    record = self._get_record_from_row([entity_id, target])
                if record is not None:
                    collection.append(record)
                    index += 1
        except KeyError as key_err:
            raise KnownException(f"Column {key_err.args[0]} could not be found in data source.") from key_err
        return collection

    def _get_record_from_row(self, row, contains_target_column=True) -> Optional[TargetFileRecord]:
        """
        Creates a record from a Subscriptable storing entity_id in index 0, target value in index 1 and date in index 2

        :param row: A subscriptable object
        :return: TargetFileRecord created from the iterable 'row'
        """
        rejected_target_classes = self._rejected_target_classes
        binary_val = BinaryTargetClass.NAN
        double_val = np.float64("nan")
        multi_class_val = "nan"

        if self._file_descriptor.target_column is not None:
            binary_target_info = self._file_descriptor.target_column.binary_target_info

            if contains_target_column:
                target = self.__get_target(row)
                if self._file_descriptor.target_column.target_column_type == AfeTargetColumnType.Binary:
                    if target == binary_target_info.positive_category:
                        binary_val = BinaryTargetClass.POSITIVE
                    elif target == binary_target_info.negative_category:
                        binary_val = BinaryTargetClass.NEGATIVE
                    elif target == binary_target_info.indeterminate_category:
                        binary_val = BinaryTargetClass.INDETERMINATE
                    elif target == binary_target_info.exclusion_category:
                        binary_val = BinaryTargetClass.EXCLUSION
                    if rejected_target_classes is not None:
                        if target in rejected_target_classes:
                            return None
                elif self._file_descriptor.target_column.target_column_type == AfeTargetColumnType.Scalar:
                    double_val = np.float64(target)
                elif self._file_descriptor.target_column.target_column_type == AfeTargetColumnType.MultiClass:
                    multi_class_val = np.object_(target)
                else:
                    raise KnownException(
                        "Unknown target type : " + self._file_descriptor.target_column.target_column_type)

        date_val = self.__get_date_value(row)
        record = TargetFileRecord()
        record.entity_id = str(row[0])
        record.event_date = date_helper.get_date_as_integer(date_val)
        record.target_binary = binary_val
        record.target_scalar = double_val
        record.target_multi_class = multi_class_val

        return record

    def __get_target(self, row):
        if self._file_descriptor.date_column is not None:
            target = str(row[2])
        else:
            target = str(row[1])
        return target

    def __get_date_value(self, row):
        if self._file_descriptor.date_column is not None:
            date_val = self._file_descriptor.default_measurement_date
            if not is_null_or_empty(self._file_descriptor.date_column.column_name):
                date_as_string = str(row[1])
                date_val = self._func(date_as_string)
        else:
            date_val = AfeStaticObjects.no_date_col_default_date
        return date_val
