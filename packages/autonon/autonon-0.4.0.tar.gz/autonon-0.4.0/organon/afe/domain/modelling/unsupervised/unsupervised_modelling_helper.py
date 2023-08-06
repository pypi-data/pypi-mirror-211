"""Includes UnsupervisedModellingHelper and UnsupervisedFeatureExtractor classes."""
from typing import List

from organon.afe.domain.modelling.unsupervised.afe_unsupervised_algorithm_settings import \
    AfeUnsupervisedAlgorithmSettings
from organon.fl.core.businessobjects.dict_dataframe import DictDataFrame
from organon.fl.modelling.unsupervised_feature_extractor import UnsupervisedFeatureExtractor


class UnsupervisedModellingHelper:
    """
    Helper class for Unsupervised Feature Extraction Service
    """

    @staticmethod
    def get_selected_cols(num_threads: int,
                          algorithm_settings: AfeUnsupervisedAlgorithmSettings = None,
                          frame_with_all_columns: DictDataFrame = None) -> List[str]:
        """Selects best afe columns by unsupervised modelling"""
        input_frame = dict((k, frame_with_all_columns.get_value(k)) for k in frame_with_all_columns.get_column_names())
        extractor = UnsupervisedFeatureExtractor(input_frame, algorithm_settings.bin_count, algorithm_settings.r_factor,
                                                 algorithm_settings.random_state, algorithm_settings.max_column_count,
                                                 algorithm_settings.is_logging)
        return extractor.execute(num_threads)
