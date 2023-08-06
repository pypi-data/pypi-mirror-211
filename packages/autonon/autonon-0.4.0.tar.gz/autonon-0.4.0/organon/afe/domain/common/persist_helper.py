"""This module includes PersistHelper class."""
from typing import List, Dict

import pandas as pd

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.domain.enums.date_resolution import DateResolution
from organon.afe.domain.modelling.businessobjects.afe_column import AfeColumn
from organon.afe.domain.modelling.businessobjects.base_afe_feature import BaseAfeFeature
from organon.afe.domain.modelling.businessobjects.transaction_file_stats import TransactionFileStats
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import string_helper


class PersistHelper:
    """Includes helper methods for persisting AFE results in db or file"""

    @classmethod
    def get_lookup_data_frame(cls, features: List[BaseAfeFeature],
                              stats: TransactionFileStats) -> pd.DataFrame:
        """Generates afe lookup data table"""
        if len(features) == 0:
            raise KnownException("Output features are empty.")

        collection_len = len(features)
        rows_per_step = max(1000, int(collection_len / 15))
        counter = 1
        rows_to_append = []
        data_frame: pd.DataFrame = None
        for item in features:
            row = cls._get_row_dict_from_feature(item, stats)
            rows_to_append.append(row)
            if counter % rows_per_step == 0 or counter == collection_len:
                if data_frame is None:
                    data_frame = pd.DataFrame(rows_to_append)
                else:
                    data_frame = pd.concat([data_frame, pd.DataFrame(rows_to_append)])
                rows_to_append.clear()
            counter += 1
        data_frame.reset_index(drop=True, inplace=True)
        return data_frame

    @classmethod
    def _get_row_dict_from_feature(cls, item: BaseAfeFeature, stats: TransactionFileStats):
        afe_column = item.afe_column
        feature_name = item.feature_name
        dimension_name = afe_column.dimension_name
        histogram = stats.get_histogram(dimension_name)
        _map = histogram.reverse_index
        feature_extended_name = PersistHelper.__get_feature_extended_name(afe_column, histogram)
        dimension_set = ""
        if afe_column.operator not in [AfeOperator.Mode, AfeOperator.CountDistinct]:
            dimension_set = afe_column.get_dimension_set(_map)
        row = {
            "FEATURE": feature_name,
            "FEATURE_EXTENDED_NAME": feature_extended_name,
            "SOURCE": afe_column.source,
            "DIMENSION": dimension_name,
            "DIMENSION_SET": dimension_set,
            "QUANTITY": afe_column.quantity_name,
            "OPERATOR": afe_column.operator.name,
            "TIME_WINDOW": afe_column.time_window,
            "RESOLUTION": afe_column.date_resolution.name,
            "DATE_OFFSET": afe_column.offset,
            "MEANING": cls.get_feature_meaning(item, _map)
        }
        if afe_column.date_column is not None:
            row["DATE_COLUMN_NAME"] = afe_column.date_column.column_name
        else:
            row["DATE_COLUMN_NAME"] = None
        return row

    @staticmethod
    def __get_feature_extended_name(afe_column, histogram):
        feature_extended_name = afe_column.build_column_name_with_map(histogram.reverse_index)
        if len(feature_extended_name) >= 100:
            feature_extended_name = feature_extended_name[:97] + "..."
        return feature_extended_name

    @staticmethod
    def print_report(selected_cols, file, d_col: str, q_col: str, name_to_column: Dict[str, AfeColumn],
                     stats: TransactionFileStats):
        """Prints model variables to file"""

        if not string_helper.is_null_or_empty(d_col) and not string_helper.is_null_or_empty(q_col):
            file.write(f"Non-interaction model for dimension column: {d_col} quantity column-{q_col}:\n")

        # file.write(f"Performance. R2:{}, AUC:{}\n")

        for column_name in selected_cols:
            afe_column = name_to_column[column_name]
            histogram = stats.get_histogram(afe_column.dimension_name)
            modified_name = afe_column.build_column_name_with_map(histogram.reverse_index)
            file.write(f"{modified_name}\n")

        file.write("\n**********************************\n")
        file.flush()

    @classmethod
    def get_feature_meaning(cls, feature: BaseAfeFeature, group_names: Dict[int, str]) -> str:
        """Returns meaning of given afe output feature"""
        afe_column = feature.afe_column
        is_not_case = not afe_column.in_out
        is_empty_case = len(afe_column.set) == 0
        qty_check = afe_column.quantity_name == AfeStaticObjects.empty_quantity_column
        dim_check = afe_column.dimension_name == AfeStaticObjects.empty_dimension_column

        operator = afe_column.operator

        before_last_dict = cls._get_before_last_dict(afe_column)

        resolution_dict = {
            DateResolution.Year: "years",
            DateResolution.Month: "months",
            DateResolution.Day: "days",
            DateResolution.Hour: "hours",
            DateResolution.Minute: "minutes",
            DateResolution.Second: "seconds"
        }

        dimension_str = afe_column.get_dimension_set(group_names)
        dimension_desc = dimension_str
        if is_not_case:
            dimension_desc = dimension_str[1:]

        where_d = ""

        if not dim_check:
            where_d = f"{afe_column.dimension_name} is {dimension_desc}"
            if is_not_case:
                where_d = f"{afe_column.dimension_name} is not {dimension_desc}"
            if not is_not_case and is_empty_case:
                where_d = f"{afe_column.dimension_name} is NULL"

        where_condition = where_d
        if not qty_check:
            if not string_helper.is_null_or_empty(where_condition):
                where_condition += " and "
            where_quantity_dict = cls._get_where_quantity_str_dict(afe_column)
            where_q = where_quantity_dict[operator]
            where_condition += where_q

        where = "" if qty_check and dim_check else "where"

        time_window_dict = cls._get_time_window_str_dict(afe_column)
        days = time_window_dict[operator]
        resolution_str = resolution_dict[DateResolution[afe_column.date_resolution.name]]

        if operator == AfeOperator.Mode:
            return f"most observed {afe_column.dimension_name} value in last {days} {resolution_str}"
        if operator == AfeOperator.CountDistinct:
            return f"Number of distinct {afe_column.dimension_name} values in last {days} {resolution_str}"
        before_last = before_last_dict[operator]
        return f"{before_last} last {days} {resolution_str} {where} {where_condition}"

    @classmethod
    def _get_before_last_dict(cls, afe_column: AfeColumn) -> Dict[AfeOperator, str]:
        quantity = afe_column.quantity_name
        if quantity and quantity != AfeStaticObjects.empty_quantity_column:
            return {
                AfeOperator.Min: f"minimum {quantity} in",
                AfeOperator.Max: f"maximum {quantity} in",
                AfeOperator.Sum: f"{quantity} sum in",
                AfeOperator.Frequency: "count in",
                AfeOperator.Ratio: f"{quantity} sum ratio in",
                AfeOperator.Density: f"{quantity} average of",
                AfeOperator.TimeSinceFirst: "time since first record in",
                AfeOperator.TimeSinceLast: "time since last record in"
            }
        return {
            AfeOperator.Min: "record count ratio of",
            AfeOperator.Max: "record count ratio of",
            AfeOperator.Sum: "record count in",
            AfeOperator.Frequency: "record count in",
            AfeOperator.Ratio: "record count ratio in",
            AfeOperator.Density: "record existing info in",
            AfeOperator.TimeSinceFirst: "time since first record in",
            AfeOperator.TimeSinceLast: "time since last record in",
        }

    @classmethod
    def _get_time_window_str_dict(cls, afe_column: AfeColumn) -> Dict[AfeOperator, str]:
        timewindow = str(afe_column.time_window)
        return {
            AfeOperator.Min: timewindow,
            AfeOperator.Max: timewindow,
            AfeOperator.Sum: timewindow,
            AfeOperator.Frequency: timewindow,
            AfeOperator.Ratio: timewindow,
            AfeOperator.Density: timewindow,
            AfeOperator.TimeSinceFirst: timewindow,
            AfeOperator.TimeSinceLast: timewindow,
            AfeOperator.Mode: timewindow,
            AfeOperator.CountDistinct: timewindow
        }

    @classmethod
    def _get_where_quantity_str_dict(cls, afe_column: AfeColumn) -> Dict[AfeOperator, str]:
        quantity = afe_column.quantity_name
        return {
            AfeOperator.Min: f"{quantity} >0",
            AfeOperator.Max: f"{quantity} >0",
            AfeOperator.Sum: f"{quantity} >0",
            AfeOperator.Frequency: f"{quantity} >0",
            AfeOperator.Ratio: f"{quantity} > 0 to where {quantity} > 0",
            AfeOperator.Density: f"{quantity} >0",
            AfeOperator.TimeSinceFirst: f"{quantity} >0",
            AfeOperator.TimeSinceLast: f"{quantity} >0"
        }
