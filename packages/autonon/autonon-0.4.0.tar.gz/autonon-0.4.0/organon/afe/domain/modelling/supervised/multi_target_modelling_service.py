"""Includes MultiTargetModellingService class."""
from typing import List, Optional

from organon.afe.domain.modelling.base_modelling_service import BaseModellingService
from organon.afe.domain.modelling.businessobjects.data_frame_builder import DataFrameBuilder
from organon.afe.domain.modelling.supervised.afe_supervised_algorithm_settings import AfeSupervisedAlgorithmSettings
from organon.afe.domain.modelling.supervised.multi_target_entity_container_service import \
    MultiTargetEntityContainerService
from organon.afe.domain.modelling.supervised.multi_target_modelling_helper import MultiTargetModellingHelper
from organon.afe.domain.settings.afe_modelling_settings import AfeModellingSettings
from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.core.businessobjects.idata_partition import IDataPartition


class MultiTargetModellingService(BaseModellingService):
    """Class for AFE modelling with multiple targets."""

    def __init__(self, settings: AfeModellingSettings):
        super().__init__(settings)
        self.modelling_helper = MultiTargetModellingHelper(self._settings)

    @staticmethod
    def _get_partition(frame_builder: DataFrameBuilder = None,
                       algorithm_settings: AfeSupervisedAlgorithmSettings = None) -> Optional[IDataPartition]:
        partition = MultiTargetModellingHelper.get_partition(frame_builder, algorithm_settings)
        return partition

    def _get_selected_cols(self, num_threads: int,
                           partition: IDataPartition = None,
                           algorithm_settings: AfeSupervisedAlgorithmSettings = None,
                           frame_builder: DataFrameBuilder = None,
                           frame_with_all_columns: DictDataFrame = None,
                           is_final=False) -> List[str]:
        return self.modelling_helper.get_selected_cols(num_threads, partition, algorithm_settings, frame_builder,
                                                       frame_with_all_columns, is_final)

    def _get_final_columns_metrics(self, num_threads: int, frame_builder: DataFrameBuilder,
                                   frame_with_all_columns: DictDataFrame, reduced_columns: List[str],
                                   algorithm_settings: AfeSupervisedAlgorithmSettings) -> dict:
        return self.modelling_helper.get_final_columns_metrics(num_threads, frame_builder, frame_with_all_columns,
                                                               reduced_columns, algorithm_settings)

    def control_target_record_files(self, multi_target_entity_container_service: MultiTargetEntityContainerService):
        self.modelling_helper.control_target_record_files(multi_target_entity_container_service)
