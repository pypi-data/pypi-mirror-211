"""Includes BaseModellingService class"""
import abc
from typing import List

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.afe.dataaccess.services.i_sample_data_service import ISampleDataService
from organon.afe.domain.modelling.abstract_modelling_service import AbstractModellingService
from organon.afe.domain.modelling.auto_column_type_decider_service import AutoColumnTypeDeciderService
from organon.afe.domain.modelling.businessobjects.afe_column import AfeColumn
from organon.afe.domain.modelling.businessobjects.afe_feature import AfeFeature
from organon.afe.domain.modelling.businessobjects.data_frame_builder import DataFrameBuilder
from organon.afe.domain.modelling.businessobjects.multi_target_entity_container import MultiTargetEntityContainer
from organon.afe.domain.modelling.businessobjects.target_file_record_collection import TargetFileRecordCollection
from organon.afe.domain.modelling.businessobjects.transaction_file_record_collection import \
    TransactionFileRecordCollection
from organon.afe.domain.reporting.afe_model_output import AfeModelOutput
from organon.afe.domain.settings.afe_modelling_settings import AfeModellingSettings
from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.helpers import list_helper
from organon.fl.logging.helpers.log_helper import LogHelper


class BaseModellingService(AbstractModellingService[AfeModellingSettings, AfeModelOutput, AfeColumn],
                           metaclass=abc.ABCMeta):
    """Base class for supervised and unsupervised modelling"""

    def __init__(self, settings: AfeModellingSettings):
        super().__init__(settings)

    @classmethod
    def _get_model_output_instance(cls) -> AfeModelOutput:
        return AfeModelOutput()

    def _control_date_column_constraint(self):
        feature_gen_settings = self._settings.data_source_settings.trx_descriptor.feature_gen_setting
        no_date_in_target_settings = self._settings.data_source_settings.target_descriptor.date_column is None
        if feature_gen_settings.date_column is not None and no_date_in_target_settings:
            raise KnownException("Since feature generation settings contain a date column, "
                                 "the target definition must have a date column")

    def _decide_dimension_and_quantity_columns(self, sample_service: ISampleDataService):
        data_source_settings = self._settings.data_source_settings
        trx_descriptor = data_source_settings.trx_descriptor

        auto_column_decider = AutoColumnTypeDeciderService(sample_service,
                                                           [trx_descriptor.feature_gen_setting],
                                                           trx_descriptor.entity_column_name,
                                                           data_source_settings.auto_column_decider_settings)

        d_columns_per_setting, q_columns_per_setting = auto_column_decider.decide_quantity_dimension_columns()
        feature_generation_settings = trx_descriptor.feature_gen_setting
        d_columns = d_columns_per_setting[0]
        q_columns = q_columns_per_setting[0]

        feature_generation_settings.dimension_columns = \
            self.__update_column_list(d_columns, AfeStaticObjects.empty_dimension_column)
        feature_generation_settings.quantity_columns = \
            self.__update_column_list(q_columns, AfeStaticObjects.empty_quantity_column)
        if feature_generation_settings.date_column is not None:
            date_col_name = feature_generation_settings.date_column.column_name
        else:
            date_col_name = " No_Date_Col - 0"
        LogHelper.info(f'Decided columns for {date_col_name} '
                       f'are \nDimension Columns:\t{feature_generation_settings.dimension_columns}'
                       f'\nQuantity Columns:\t{feature_generation_settings.quantity_columns}')

    def _get_non_empty_date_columns_dict(self):
        date_col = self._settings.data_source_settings.trx_descriptor.feature_gen_setting.date_column
        if date_col is not None:
            return {date_col.column_name: date_col}
        return {}

    def _get_interval_per_entity_per_date_col(self, multi_target_entity_container: MultiTargetEntityContainer):
        interval_per_entity_per_date_col = {}
        feature_generation_settings = self._settings.data_source_settings.trx_descriptor.feature_gen_setting

        if feature_generation_settings.date_column is not None:
            interval_per_entity = multi_target_entity_container.get_date_interval_per_entity(
                feature_generation_settings.date_resolution, max(feature_generation_settings.horizon_list),
                feature_generation_settings.date_offset)
            interval_per_entity_per_date_col[feature_generation_settings.date_column.column_name] \
                = interval_per_entity
        return interval_per_entity_per_date_col

    def _get_output_features(self, reduced_columns_list: List[AfeColumn]):
        output_features = {}
        for i, col in enumerate(reduced_columns_list):
            feature_name = f"{self._settings.output_settings.feature_name_prefix}_{i}"
            feature = AfeFeature(col)
            feature.feature_name = feature_name
            output_features[feature_name] = feature
        return output_features

    def _get_data_frame_builder(self, target_file_record_collection: TargetFileRecordCollection,
                                trx_file_record_collection: TransactionFileRecordCollection):
        all_dimensions, all_horizons = {}, {}
        data_source_settings = self._settings.data_source_settings
        feature_generation_settings = data_source_settings.trx_descriptor.feature_gen_setting
        all_dimensions[0] = set(feature_generation_settings.dimension_columns)
        all_horizons[0] = set(feature_generation_settings.horizon_list)

        frame_builder = DataFrameBuilder(data_source_settings.target_descriptor,
                                         target_file_record_collection,
                                         trx_file_record_collection,
                                         dimensions_per_date_col=all_dimensions,
                                         horizons_per_date_col=all_horizons)
        return frame_builder

    def _reduce_for_settings(self, frame_builder, all_columns_frame, reduction_settings, file):
        trx_descriptor = self._settings.data_source_settings.trx_descriptor
        partition = self._reduce_for_feature_gen_setting(frame_builder, 0,
                                                         trx_descriptor.feature_gen_setting, reduction_settings,
                                                         all_columns_frame, None, file)
        return partition

    @staticmethod
    def __update_column_list(base_list: List[str], new_column: str) -> List[str]:
        if list_helper.is_null_or_empty(base_list):
            return [new_column]
        base_list.append(new_column)
        return list(set(base_list))
