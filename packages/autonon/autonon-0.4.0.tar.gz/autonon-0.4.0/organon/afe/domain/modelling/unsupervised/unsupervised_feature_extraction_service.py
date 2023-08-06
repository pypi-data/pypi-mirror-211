"""
This module is for unsupervised feature extraction
"""
from typing import List

from organon.afe.domain.modelling.base_modelling_service import BaseModellingService
from organon.afe.domain.modelling.businessobjects.data_frame_builder import DataFrameBuilder
from organon.afe.domain.modelling.unsupervised.afe_unsupervised_algorithm_settings import \
    AfeUnsupervisedAlgorithmSettings
from organon.afe.domain.modelling.unsupervised.unsupervised_modelling_helper import UnsupervisedModellingHelper
from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.core.businessobjects.idata_partition import IDataPartition


class UnsupervisedFeatureExtractionService(BaseModellingService):
    """
    Class for Unsupervised Feature Extraction Service
    """

    def _get_selected_cols(self, num_threads: int,
                           partition: IDataPartition = None,
                           algorithm_settings: AfeUnsupervisedAlgorithmSettings = None,
                           frame_builder: DataFrameBuilder = None,
                           frame_with_all_columns: DictDataFrame = None,
                           is_final=False) -> List[str]:
        return UnsupervisedModellingHelper.get_selected_cols(num_threads, algorithm_settings, frame_with_all_columns)
