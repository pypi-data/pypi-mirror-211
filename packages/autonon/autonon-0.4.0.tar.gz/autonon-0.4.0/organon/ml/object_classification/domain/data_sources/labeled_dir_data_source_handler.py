"""Includes LabeledDirDataSourceHandler class"""
import os
from typing import List

import numpy as np
from pandas import DataFrame

from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.common.enums.color_type import ColorType
from organon.ml.object_classification.common.helpers import \
    throw_val_ex_with_log
from organon.ml.object_classification.common.object_classification_constants import \
    ObjectClassificationConstants
from organon.ml.object_classification.domain.data_sources.base_data_source_handler import \
    BaseDataSourceHandler
from organon.ml.object_classification.domain.objects.data_source_settings import \
    DataSourceSettings


class LabeledDirDataSourceHandler(BaseDataSourceHandler[str]):
    """Class for handling labeled directory input"""

    def __init__(self, data: str, settings: DataSourceSettings):
        super().__init__(data, settings)
        self.filenames: List[str] = None

    def process_data(self):
        import tensorflow as tf # pylint: disable=import-outside-toplevel
        self.filenames = self._get_labeled_dir_filenames(self.data)

        label_mode = "binary" if self.settings.clf_type == ClassificationType.BINARY else "categorical"
        self._dataset = tf.keras.utils.image_dataset_from_directory(directory=self.data,
                                                                    batch_size=self.settings.batch_size,
                                                                    image_size=self.settings.image_size,
                                                                    shuffle=False, seed=self.settings.random_seed,
                                                                    color_mode=self._get_color_parameter(),
                                                                    label_mode=label_mode)

    def initialize_probs_df(self) -> DataFrame:
        return DataFrame({ObjectClassificationConstants.FILENAME_COL_NAME: self.filenames,
                          ObjectClassificationConstants.LABELS_COL_NAME: self.get_labels()})

    def _get_color_parameter(self) -> str:
        if self.settings.color_mode == ColorType.RGB:
            color_mode = "rgb"
        elif self.settings.color_mode == ColorType.RGBA:
            color_mode = "rgba"
        elif self.settings.color_mode == ColorType.GRAY:
            color_mode = "grayscale"
        else:
            return throw_val_ex_with_log("Color mode is not defined!")
        return color_mode

    @staticmethod
    def _get_labeled_dir_filenames(directory: str) -> List[str]:
        files = [file for _, _, file in os.walk(
            directory)]  # image_dataset_from_directory ile aynı sırada geliyor, o fonksiyon da os.walk kullanıyor
        return list(np.concatenate(files).flat)

    def _get_binary_labels(self):
        labels = self._extract_labels()
        return labels.flatten()

    def _get_multiclass_labels(self):
        return np.argmax(np.concatenate(self._extract_labels(), axis=0), axis=1)
