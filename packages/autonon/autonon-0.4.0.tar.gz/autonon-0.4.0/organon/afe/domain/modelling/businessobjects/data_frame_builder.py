"""This module includes DataFrameBuilder class."""
import copy
import math
from typing import Dict, List

import numpy as np
import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.dataaccess.services.transaction_file_record_reader import TransactionFileRecordReader
from organon.afe.domain.enums.afe_operator import AfeOperator, OPERATOR_SET_ONE, OPERATOR_SET_TWO
from organon.afe.domain.enums.afe_target_column_type import AfeTargetColumnType
from organon.afe.domain.enums.binary_target_class import BinaryTargetClass
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.modelling.businessobjects.afe_column import AfeColumn
from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats
from organon.afe.domain.modelling.helper import data_frame_builder_helper  # pylint: disable=no-name-in-module
from organon.afe.domain.settings.afe_date_column import AfeDateColumn
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.afe.domain.settings.target_descriptor import TargetDescriptor
from organon.fl.core.businessobjects.histogram_16 import Histogram16
from organon.fl.core.businessobjects.np2d_dataframe import Np2dDataFrame
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import date_helper
from organon.fl.logging.helpers.log_helper import LogHelper


# pylint: disable=too-many-instance-attributes
class DataFrameBuilder:
    """Class for generating AFE features and building a dataframe which stores feature values for every entity."""

    operators = [AfeOperator.Sum, AfeOperator.Max, AfeOperator.Min, AfeOperator.Frequency,
                 AfeOperator.Density, AfeOperator.CountDistinct, AfeOperator.Mode,
                 AfeOperator.TimeSinceLast, AfeOperator.TimeSinceFirst, AfeOperator.Ratio]

    # pylint: disable=too-many-arguments
    def __init__(self,
                 target_descriptor: TargetDescriptor,
                 target_file_record_collection: TargetFileRecordCollection,
                 trx_file_record_collection: TransactionFileRecordCollection,
                 transaction_file_stats: TransactionFileStats = None,
                 dimensions_per_date_col: Dict[int, set] = None,
                 horizons_per_date_col: Dict[int, set] = None,
                 max_num_of_columns: int = None
                 ):

        self._target_descriptor = target_descriptor
        self._target_file_record_collection = target_file_record_collection
        self._trx_file_record_collection = trx_file_record_collection
        self._dimensions_per_date_col = dimensions_per_date_col
        self._horizons_per_date_col = horizons_per_date_col
        if transaction_file_stats is None:
            self._trx_stats = trx_file_record_collection.transaction_file_stats
        else:
            self._trx_stats = transaction_file_stats

        if max_num_of_columns is None:
            if dimensions_per_date_col is None or horizons_per_date_col is None is None:
                raise KnownException("Please supply dimensions_per_date_col, horizons_per_date_col"
                                     " to calculate max number of columns")
            max_num_of_columns = self._get_maximum_number_of_frame_columns()

        if target_file_record_collection is not None:
            self._frame = Np2dDataFrame(target_file_record_collection.sampled_count,
                                        max_num_of_columns, np.float32)

        self.target_array: np.array = None
        self._record_index_target_index_map: Dict[int, str] = {}
        self._name_to_column: Dict[str, AfeColumn] = {}
        self._group_to_name: Dict[str, List[str]] = {}
        self._index_to_id: Dict[int, str] = None
        self._index_to_date: Dict[int, int] = None
        self._included_operators = None
        self._included_operator_set_one = None
        self._included_operator_set_two = None
        self._new_col_names_map: Dict[str, str] = {}

    @property
    def frame(self):
        """Returns dataframe."""
        return self._frame

    @property
    def name_to_column(self):
        """Returns 'column name - AfeColumn instance' mapping."""
        return self._name_to_column

    @property
    def index_to_id(self):
        """Returns 'dataframe index - entity_id' mapping."""
        return self._index_to_id

    @property
    def new_col_names_map(self):
        """Returns 'dataframe index - event_date' mapping."""
        return self._new_col_names_map

    @property
    def index_to_date(self) -> Dict[int, int]:
        """Returns 'dataframe index - event_date' mapping."""
        return self._index_to_date

    @property
    def trx_file_record_collection(self) -> TransactionFileRecordCollection:
        """Returns trx_file_record_collection used for frame building."""
        return self._trx_file_record_collection

    def _set_included_operators(self, included_operators: List[AfeOperator],
                                dimension_column: str, quantity_column: str,
                                remove_operators_used_no_date: bool = False):
        self._included_operators = included_operators
        DataFrameBuilder._remove_operators_by_qty_and_dim(dimension_column, quantity_column,
                                                          self._included_operators)

        self._included_operator_set_one = list(
            set(OPERATOR_SET_ONE) & set(included_operators))
        self._included_operator_set_two = list(
            set(OPERATOR_SET_TWO) & set(included_operators))
        if remove_operators_used_no_date:
            DataFrameBuilder.__remove_operators_used_no_date(self._included_operator_set_two)

    def execute(self, num_of_threads: int, dimension_column: str, quantity_column: str,
                feature_generation_settings: FeatureGenerationSettings):
        """Generates dataframe by calculating AFE features and values for every entity"""

        trx_record_collection = self._trx_file_record_collection
        included_operators = feature_generation_settings.included_operators.copy()
        remove_operators_used_no_date = False
        if feature_generation_settings.date_column is None:
            remove_operators_used_no_date = True
        self._set_included_operators(included_operators, dimension_column, quantity_column,
                                     remove_operators_used_no_date)
        horizons = feature_generation_settings.horizon_list
        horizons.sort()
        histogram = self._trx_stats.get_histogram(dimension_column)
        nearest_exponent = self.__get_nearest_exponent(histogram.original_to_compressed, horizons)
        date_column = None
        date_column_index = -1
        if feature_generation_settings.date_column is not None:
            date_column = feature_generation_settings.date_column
            date_column_index = trx_record_collection.date_col_map[date_column.column_name]

        hash_column_map = self._add_columns_to_frame(horizons,
                                                     date_column,
                                                     feature_generation_settings.date_resolution,
                                                     feature_generation_settings.date_offset,
                                                     dimension_column,
                                                     quantity_column, nearest_exponent)

        splits = DataFrameBuilder._split(self._target_file_record_collection, num_of_threads)
        self._set_index_mappings(splits)

        new_entity_index_map = self._get_new_entity_index_map(splits, trx_record_collection.entity_index_map)

        # pylint: disable=c-extension-no-member
        data_frame_builder_helper.execute(
            self._frame.data_frame,
            num_of_threads,
            date_column_index,
            trx_record_collection.d_map[dimension_column],
            trx_record_collection.q_map[quantity_column],
            splits,
            horizons,
            feature_generation_settings.date_offset,
            feature_generation_settings.date_resolution.value,
            histogram.original_to_compressed,
            trx_record_collection.dates,
            trx_record_collection.q_arrays,
            trx_record_collection.d_arrays,
            new_entity_index_map,
            self._target_file_record_collection.event_dates,
            [a.value for a in self._included_operators],
            [a.value for a in self._included_operator_set_one],
            [a.value for a in self._included_operator_set_two],
            hash_column_map,
            nearest_exponent
        )
        if self._target_descriptor.target_column is not None:
            if self.target_array is None:
                self._generate_target()

    def _get_new_entity_index_map(self, splits, entity_index_map):
        new_entity_index_map = {}
        for i in range(splits.shape[0]):
            for j in range(splits.shape[1]):
                frame_index = i + j * splits.shape[0]
                record_index = splits[i][j]
                if record_index != -1:
                    entity = self._target_file_record_collection.entities[record_index]
                    if entity in entity_index_map:
                        new_entity_index_map[record_index] = entity_index_map[entity]
                    self._record_index_target_index_map[frame_index] = record_index
        return new_entity_index_map

    @staticmethod
    def _remove_operators_by_qty_and_dim(dimension_column: str, quantity_column: str,
                                         included_operators: List[AfeOperator]):
        if quantity_column != AfeStaticObjects.empty_quantity_column or \
                dimension_column == AfeStaticObjects.empty_dimension_column:
            if AfeOperator.Mode in included_operators:
                included_operators.remove(AfeOperator.Mode)
            if AfeOperator.CountDistinct in included_operators:
                included_operators.remove(AfeOperator.CountDistinct)

    @staticmethod
    def __remove_operators_used_no_date(included_operator_set_two):
        remove_included_operator_set_two = OPERATOR_SET_TWO
        for operator in remove_included_operator_set_two:
            if operator in included_operator_set_two:
                included_operator_set_two.remove(operator)

    def execute_for_afe_columns(self, num_of_threads: int, afe_columns: Dict[str, BaseAfeFeature]):
        """Builds dataframe by aggregating data according to given afe columns."""

        counter = 0

        splits = DataFrameBuilder._split(self._target_file_record_collection, num_of_threads)
        self._set_index_mappings(splits)

        column_index_name_map: Dict[int, str] = {}
        for date_col, afe_columns_for_date_col in self._group_features_by_date_column(afe_columns).items():
            if date_col is not None:
                self._trx_file_record_collection.sort(date_col)

            # entity_index_map should be regenerated after sorting trx_file entity index map
            new_entity_index_map = self._get_new_entity_index_map(splits,
                                                                  self._trx_file_record_collection.entity_index_map)

            for feature_name, feature in afe_columns_for_date_col.items():
                afe_column = feature.afe_column
                counter += 1
                dim_group_id = afe_column.group_id
                date_col_name = afe_column.date_column.column_name if afe_column.date_column is not None else ""
                LogHelper.info(f"Frame builder executing for afe column {counter}/{len(afe_columns)} : "
                               f"{afe_column.dimension_name}-{dim_group_id}-"
                               f"{afe_column.quantity_name}-{afe_column.operator}-"
                               f"{date_col_name}-{afe_column.time_window}")

                op_to_calculate = afe_column.operator

                included_operators = [op_to_calculate] if op_to_calculate in self.operators else []

                self._set_included_operators(included_operators, afe_column.dimension_name,
                                             afe_column.quantity_name)

                horizons = [afe_column.time_window]

                histogram = self._trx_stats.get_histogram(afe_column.dimension_name)
                nearest_exponent = self.__get_nearest_exponent(histogram.original_to_compressed, horizons)

                hash_val, column_index = self._add_column_to_frame_for_feature(feature, nearest_exponent)
                column_index_name_map[column_index] = feature_name

                date_column_index = -1
                if afe_column.date_column is not None:
                    date_column_index = \
                        self._trx_file_record_collection.date_col_map[afe_column.date_column.column_name]

                original_to_compressed = histogram.original_to_compressed.copy()
                original_to_compressed[np.int16(TransactionFileRecordReader.UNKNOWN_DIMENSION_VALUE)] = \
                    np.int16(TransactionFileRecordReader.UNKNOWN_DIMENSION_VALUE)

                # pylint: disable=c-extension-no-member
                data_frame_builder_helper.execute(
                    self._frame.data_frame,
                    num_of_threads,
                    date_column_index,
                    self._trx_file_record_collection.d_map[afe_column.dimension_name],
                    self._trx_file_record_collection.q_map[afe_column.quantity_name],
                    splits,
                    horizons,
                    afe_column.offset,
                    afe_column.date_resolution.value,
                    original_to_compressed,
                    self._trx_file_record_collection.dates,
                    self._trx_file_record_collection.q_arrays,
                    self._trx_file_record_collection.d_arrays,
                    new_entity_index_map,
                    self._target_file_record_collection.event_dates,
                    [a.value for a in self._included_operators],
                    [a.value for a in self._included_operator_set_one],
                    [a.value for a in self._included_operator_set_two],
                    {hash_val: column_index},
                    nearest_exponent,
                    dim_group_id if dim_group_id is not None else -1,
                    True,
                    afe_column.dimension_name == AfeStaticObjects.empty_dimension_column
                )
        self._update_column_names_in_frame(column_index_name_map)

    def _update_column_names_in_frame(self, column_index_name_map: Dict[int, str]):
        new_col_names_map = {}
        for col_index, feature_name in column_index_name_map.items():
            old_name = self._frame.get_column_name_by_index(col_index)
            new_col_names_map[old_name] = feature_name
        self._new_col_names_map = new_col_names_map
        self._frame.rename_columns(new_col_names_map)

    @staticmethod
    def _group_features_by_date_column(afe_columns: Dict[str, BaseAfeFeature]) -> Dict[str, Dict[str, BaseAfeFeature]]:
        features_grouped_by_date_col = {}

        for feature_name, feature in afe_columns.items():
            date_col_name = feature.afe_column.date_column.column_name \
                if feature.afe_column.date_column is not None else None
            if date_col_name in features_grouped_by_date_col:
                features_grouped_by_date_col[date_col_name][feature_name] = feature
            else:
                features_grouped_by_date_col[date_col_name] = {feature_name: feature}
        return features_grouped_by_date_col

    def get_frame_as_pandas_dataframe(self) -> pd.DataFrame:
        """Returns frame as pandas dataframe with additional entity id and event date columns"""
        data_frame = pd.DataFrame()

        record_indices = [self._record_index_target_index_map[i] for i in range(self._frame.data_frame.shape[0])]
        entities = [self._target_file_record_collection.entities[i] for i in record_indices]
        data_frame[AfeStaticObjects.distinct_entities_entity_column_name] = entities

        if self._target_descriptor.date_column is not None:
            dates = [date_helper.get_integer_as_date(self._target_file_record_collection.event_dates[i]) for i in
                     record_indices]
            data_frame[AfeStaticObjects.event_date_column_name] = dates

        for col in self._frame.column_name_map:
            data_frame[col] = self._frame.get_value(col)
        return data_frame

    def _set_index_mappings(self, splits: np.ndarray):
        self._index_to_id = {}
        self._index_to_date = {}
        for i in range(splits.shape[0]):
            for j in range(splits.shape[1]):
                index = i + j * splits.shape[0]
                record_index: int = splits[i][j]
                if record_index != -1:
                    entity_id = self._target_file_record_collection.entities[record_index]
                    date = self._target_file_record_collection.event_dates[record_index]
                    self._index_to_id[index] = entity_id
                    self._index_to_date[index] = date

    def _get_maximum_number_of_frame_columns(self):
        max_count = 0
        for date_col in self._dimensions_per_date_col:
            num_horizons = len(self._horizons_per_date_col[date_col])
            count = (len(OPERATOR_SET_ONE) + 1) * num_horizons + len(OPERATOR_SET_TWO)

            max_num_of_dimension_groups = 0
            for dimension_column in self._dimensions_per_date_col[date_col]:
                histogram = self._trx_stats.get_histogram(dimension_column)
                num_groups_for_dimension = len(histogram.compressed_reverse_index)
                if num_groups_for_dimension > max_num_of_dimension_groups:
                    max_num_of_dimension_groups = num_groups_for_dimension
            max_for_date_col = count * max_num_of_dimension_groups
            max_count = max(max_for_date_col, max_count)
        return int(max_count + 1)  # +1 for target column

    def _add_column_to_frame_for_feature(self, feature: BaseAfeFeature, nearest_exponent: int):
        hash_column_map = {}
        stats = self._trx_stats
        histogram = stats.get_histogram(feature.afe_column.dimension_name)
        date_col_name = self._get_date_col_name_of_afe_column(feature.afe_column)
        date_column = AfeDateColumn(column_name=date_col_name)
        afe_column = self._get_base_afe_column_instance(date_column, feature.afe_column.dimension_name,
                                                        feature.afe_column.quantity_name,
                                                        feature.afe_column.date_resolution, feature.afe_column.offset)

        operator = feature.afe_column.operator
        horizon = feature.afe_column.time_window
        allowed_dim_values = None if feature.afe_column.group_id is None else [feature.afe_column.group_id]
        if operator in self._included_operator_set_one:
            afe_column.operator = operator
            afe_column.time_window = horizon
            self._add_columns_to_frame_with_indices(afe_column, histogram, nearest_exponent, hash_column_map,
                                                    allowed_dim_values)
        elif operator in self._included_operator_set_two:
            afe_column.operator = operator
            afe_column.time_window = horizon
            self._add_columns_to_frame_with_indices(afe_column, histogram, nearest_exponent, hash_column_map,
                                                    allowed_dim_values)
        elif AfeOperator.Ratio in self._included_operators:
            afe_column.operator = AfeOperator.Ratio
            afe_column.time_window = horizon
            self._add_columns_to_frame_with_indices(afe_column, histogram, nearest_exponent, hash_column_map,
                                                    allowed_dim_values)

        return next(iter(hash_column_map.items()))

    def _add_columns_to_frame(self, horizons: List[int],
                              date_column: AfeDateColumn, resolution: DateResolution, offset: int,
                              dimension_name: str, quantity_name: str,
                              nearest_exponent: int,
                              allowed_dim_values: List[int] = None):
        # pylint: disable=too-many-arguments
        hash_column_map = {}
        max_horizon = max(horizons)
        stats = self._trx_stats
        histogram = stats.get_histogram(dimension_name)
        afe_column = self._get_base_afe_column_instance(date_column, dimension_name, quantity_name, resolution, offset)
        for operator in self._included_operator_set_one:
            for horizon in horizons:
                afe_column.operator = operator
                afe_column.time_window = horizon
                self._add_columns_to_frame_with_indices(afe_column, histogram, nearest_exponent, hash_column_map,
                                                        allowed_dim_values)
        for operator in self._included_operator_set_two:
            afe_column.operator = operator
            afe_column.time_window = max_horizon
            self._add_columns_to_frame_with_indices(afe_column, histogram, nearest_exponent, hash_column_map,
                                                    allowed_dim_values)
        if AfeOperator.Ratio in self._included_operators:
            afe_column.operator = AfeOperator.Ratio
            for horizon in horizons:
                afe_column.time_window = horizon
                self._add_columns_to_frame_with_indices(afe_column, histogram, nearest_exponent, hash_column_map,
                                                        allowed_dim_values)

        return hash_column_map

    @classmethod
    def _get_base_afe_column_instance(cls, date_column: AfeDateColumn, dimension_name: str,
                                      quantity_name: str, resolution: DateResolution, offset: int) -> AfeColumn:
        afe_column = AfeColumn()
        afe_column.date_column = date_column
        afe_column.dimension_name = dimension_name
        afe_column.quantity_name = quantity_name
        afe_column.date_resolution = resolution
        afe_column.offset = offset
        return afe_column

    def _add_columns_to_frame_with_indices(self, base_afe_column: AfeColumn, histogram: Histogram16,
                                           nearest_exponent: int,
                                           hash_column_map: Dict[int, int],
                                           allowed_dim_values: List[int] = None):

        entire_index_list = list(histogram.index.values())
        for key, value in histogram.compressed_reverse_index.items():
            afe_column = copy.deepcopy(base_afe_column)
            group_id = key
            if allowed_dim_values and group_id not in allowed_dim_values:
                continue
            list_of_values = value
            dim_values = []
            for item in list_of_values:
                dim_values.append(histogram.index[item])

            complement = [x for x in entire_index_list if x not in dim_values]
            in_out = True
            if complement:
                in_out = len(dim_values) < len(complement)

            afe_column.group_id = group_id
            afe_column.set = dim_values if in_out else complement
            afe_column.in_out = in_out
            afe_column.set_column_name()

            column_name = afe_column.column_name
            group_name = afe_column.get_group_name()

            self._name_to_column[column_name] = afe_column
            if group_name not in self._group_to_name:
                self._group_to_name[group_name] = []
            self._group_to_name[group_name].append(column_name)

            self._frame.try_add(column_name)
            col_index = self._frame.column_name_map[column_name]

            self._add_column_to_map(hash_column_map, afe_column, col_index, nearest_exponent)

    @staticmethod
    def _split(collection: TargetFileRecordCollection, num_of_threads: int) -> \
            np.ndarray:
        _dict = np.full((num_of_threads, math.ceil(collection.sampled_count / num_of_threads)), -1, dtype=np.int32)

        if collection.sampled:
            indices = collection.indices
            for i, index in enumerate(indices):
                _dict[i % num_of_threads][math.floor(i / num_of_threads)] = index
        else:
            for i in range(collection.sampled_count):
                _dict[i % num_of_threads][math.floor(i / num_of_threads)] = i
        return _dict

    def clean_frame(self):
        """removes all columns from frame which are not in 'stayers'(except 'target_column')"""
        for column_name in self._frame.get_column_names():
            self._frame.remove(column_name)

    def _generate_target(self):
        record_count = self._target_file_record_collection.sampled_count
        base_target_column = self._target_descriptor.target_column
        target_column_type = base_target_column.target_column_type
        if target_column_type == AfeTargetColumnType.Binary:
            target_array = []
            positive_category = base_target_column.binary_target_info.positive_category
            negative_category = base_target_column.binary_target_info.negative_category
            if self._target_file_record_collection.sampled:
                indices: np.array = self._target_file_record_collection.indices
                for index in indices:
                    target_binary = self._target_file_record_collection.target_binary_values[index]
                    target_val = positive_category if target_binary == BinaryTargetClass.POSITIVE.value \
                        else negative_category
                    target_array.append(target_val)
            else:
                for i in range(record_count):
                    target_binary = self._target_file_record_collection.target_binary_values[i]
                    target_val = positive_category if target_binary == BinaryTargetClass.POSITIVE.value \
                        else negative_category
                    target_array.append(target_val)

            self.target_array = np.array(target_array)
        elif target_column_type == AfeTargetColumnType.Scalar:
            self.__generate_target_for_multi_class_and_scalar(
                record_count, self._target_file_record_collection.target_scalar_values)
        elif target_column_type == AfeTargetColumnType.MultiClass:
            self.__generate_target_for_multi_class_and_scalar(
                record_count, self._target_file_record_collection.target_multi_class_values)
        else:
            raise KnownException("Unknown target type :" + str(target_column_type))

    def __generate_target_for_multi_class_and_scalar(self, record_count: int, target_values):
        target_array = []
        if self._target_file_record_collection.sampled:
            indices = self._target_file_record_collection.indices
            for index in indices:
                target_array.append(target_values[index])
        else:
            for i in range(record_count):
                target_array.append(target_values[i])
        self.target_array = np.array(target_array)

    @staticmethod
    def __get_nearest_exponent(index_map: Dict, horizons):
        max_index_map_val = max(index_map.values())
        max_afe_operator_val = max([a.value for a in AfeOperator])
        max_val = max([max_index_map_val, max_afe_operator_val, max(horizons)])
        nearest_exponent = 10 ** (math.floor(math.log10(max_val)) + 1)
        return nearest_exponent

    @staticmethod
    def _add_column_to_map(hash_column_map, base_afe_column: AfeColumn, col_index, nearest_exponent: int):
        val = (nearest_exponent ** 2 * base_afe_column.group_id) + \
              (nearest_exponent ** 1 * base_afe_column.operator.value) + \
              base_afe_column.time_window
        hash_column_map[val] = col_index
        return col_index

    @staticmethod
    def _get_date_col_name_of_afe_column(afe_col: AfeColumn):
        return afe_col.date_column.column_name if afe_col.date_column is not None else ""
