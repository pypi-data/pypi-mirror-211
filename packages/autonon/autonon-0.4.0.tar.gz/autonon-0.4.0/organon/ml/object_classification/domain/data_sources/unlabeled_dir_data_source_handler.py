"""Includes UnlabeledDirDataSourceHandler class"""
import os

from pandas import DataFrame

from organon.ml.object_classification.common.object_classification_constants import \
    ObjectClassificationConstants
from organon.ml.object_classification.domain.data_sources.base_data_source_handler import \
    BaseDataSourceHandler


class UnlabeledDirDataSourceHandler(BaseDataSourceHandler[str]):
    """Class for handling Unlabeled Directory input"""

    def process_data(self):
        import tensorflow as tf # pylint: disable=import-outside-toplevel

        def parse_image(filename):
            parts = tf.strings.split(filename, os.sep)
            label = parts[-1]
            image = tf.io.read_file(filename)
            image = tf.io.decode_jpeg(image)
            return image, label

        list_ds = tf.data.Dataset.list_files(os.path.join(self.data, "*.*"))
        self._dataset = list_ds.map(parse_image)
        self._transform_tf_dataset()

    def initialize_probs_df(self) -> DataFrame:
        return DataFrame({ObjectClassificationConstants.FILENAME_COL_NAME: self.get_labels()})

    def _get_binary_labels(self):
        return [label.numpy().decode() for label in self._extract_labels()]

    def _get_multiclass_labels(self):
        return [label.numpy().decode() for label in self._extract_labels()]
