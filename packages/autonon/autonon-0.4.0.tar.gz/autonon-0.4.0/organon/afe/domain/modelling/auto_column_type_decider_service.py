"""
This module contains AutoColumnTypeDeciderService for detecting quantity and dimension columns.
"""

from typing import Set, List, Tuple, Dict

import pandas as pd

from organon.afe.dataaccess.services.i_sample_data_service import ISampleDataService
from organon.afe.domain.settings.auto_column_decider_settings import AutoColumnDeciderSettings
from organon.afe.domain.settings.feature_generation_settings import FeatureGenerationSettings
from organon.fl.core.helpers import list_helper


class AutoColumnTypeDeciderService:
    """
    This class creates gets sample frame and decides quantity and dimension columns in that frame.
    """

    def __init__(self, sample_service: ISampleDataService,
                 feature_gen_settings: List[FeatureGenerationSettings],
                 trx_entity_col_name: str,
                 auto_decider_settings: AutoColumnDeciderSettings):
        self.frame = None
        self.__sample_service = sample_service

        self.__feature_gen_settings = feature_gen_settings
        self.__trx_entity_column = trx_entity_col_name

        self.__trx_date_columns = [setting.date_column.column_name
                                   for setting in feature_gen_settings
                                   if getattr(setting, "date_column") is not None]

        self.__numeric_to_dimension = auto_decider_settings.numeric_to_dimension
        self.__dimension_distinct_cut_off = auto_decider_settings.dimension_distinct_cut_off

        self.__rejected_quantity_columns = auto_decider_settings.rejected_quantity_columns
        self.__use_quantity_columns = auto_decider_settings.use_quantity_columns

        self.__rejected_dimension_columns = auto_decider_settings.rejected_dimension_columns
        self.__use_dimension_columns = auto_decider_settings.use_dimension_columns

    def decide_quantity_dimension_columns(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        This function handles the logic for auto deciding for quantity and dimension columns
        """
        q_columns_per_setting, d_extra_per_setting = self.decide_quantity_columns()
        d_columns_per_setting = self.decide_dimension_columns(d_extra_per_setting)

        return d_columns_per_setting, q_columns_per_setting

    def decide_quantity_columns(self) -> Tuple[Dict[str, List[str]], Dict[str, Set[str]]]:
        """
        This method handles the logic for deciding quantity columns according to settings
        :return: quantity columns and extra columns to be added to dimension columns
        """
        q_columns_per_setting = {}
        d_extra_per_setting = {}
        q_columns_from_frame = None
        d_extra_from_frame = None

        for order, setting in enumerate(self.__feature_gen_settings):
            q_columns = set()
            d_extra = set()
            if not list_helper.is_null_or_empty(setting.quantity_columns):
                q_columns.update(setting.quantity_columns)
            elif not self.__use_quantity_columns:
                pass
            else:
                if self.frame is None:
                    self.frame = self.__sample_service.get_sample()
                if q_columns_from_frame is None:
                    q_columns_from_frame, d_extra_from_frame = self.__get_quantity_columns()
                q_columns, d_extra = q_columns_from_frame, d_extra_from_frame
            q_columns.difference_update(set(self.__rejected_quantity_columns))
            q_columns_per_setting[order] = list(q_columns)
            d_extra_per_setting[order] = d_extra

        return q_columns_per_setting, d_extra_per_setting

    def decide_dimension_columns(self, d_extra: Dict[str, Set[str]]) -> Dict[str, List[str]]:
        """
        This method handles the logic for deciding dimension columns according to settings
        :param d_extra: extra columns to be added to dimension columns
        :return: list of dimension columns
        """
        d_cols_per_setting = {}
        d_columns_from_frame = None
        for order, setting in enumerate(self.__feature_gen_settings):
            d_columns = set()
            if not list_helper.is_null_or_empty(setting.dimension_columns):
                d_columns.update(setting.dimension_columns)
            elif not self.__use_dimension_columns:
                pass
            else:
                if self.frame is None:
                    self.frame = self.__sample_service.get_sample()
                if d_columns_from_frame is None:
                    d_columns_from_frame = self.__get_dimension_columns()
                d_columns = d_columns_from_frame
            d_columns.update(d_extra[order])
            d_columns.difference_update(set(self.__rejected_dimension_columns))
            d_cols_per_setting[order] = list(d_columns)
        return d_cols_per_setting

    def __get_quantity_columns(self) -> Tuple[Set[str], Set[str]]:
        """
        This function detects quantity columns in frame
        :return: quantity columns and extra columns to be added to dimension columns
        """
        q_columns: Set[str] = set()
        d_extra_columns: Set[str] = set()

        for column_name in self.frame:
            column = self.frame[column_name]
            if not pd.core.dtypes.common.is_datetime_or_timedelta_dtype(column) and \
                    pd.to_numeric(column, errors='coerce').notnull().all():
                distinct_count = column.nunique()
                if distinct_count < self.__numeric_to_dimension and not pd.api.types.is_float(column):
                    d_extra_columns.add(column_name)
                else:
                    q_columns.add(column_name)

        q_columns.difference_update(self.__trx_date_columns + [self.__trx_entity_column])
        d_extra_columns.difference_update(self.__trx_date_columns + [self.__trx_entity_column])

        return q_columns, d_extra_columns

    def __get_dimension_columns(self) -> Set[str]:
        """
        This function detects dimension columns in frame
        :return: dimension columns
        """
        d_columns: Set[str] = set()

        n_rows = len(self.frame)

        for column_name in self.frame:
            column = self.frame[column_name]
            if not pd.api.types.is_numeric_dtype(column) and not pd.api.types.is_datetime64_any_dtype(column):
                d_columns.add(column_name)

        for column_name in d_columns.copy():
            column = self.frame[column_name]
            distinct_count = column.nunique()
            if distinct_count / n_rows > self.__dimension_distinct_cut_off:
                d_columns.remove(column_name)

        d_columns.difference_update(self.__trx_date_columns + [self.__trx_entity_column])

        return d_columns
