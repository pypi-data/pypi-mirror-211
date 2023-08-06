"""Includes TfDatasetDataSourceHandler class"""
from typing import TYPE_CHECKING

from pandas import DataFrame

from organon.ml.object_classification.common.object_classification_constants import \
    ObjectClassificationConstants
from organon.ml.object_classification.domain.data_sources.base_data_source_handler import \
    BaseDataSourceHandler, _DataSourceDataTypeT
from organon.ml.object_classification.domain.objects.data_source_settings import DataSourceSettings

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class TfDatasetDataSourceHandler(BaseDataSourceHandler["tf.data.Dataset"]):
    """Class for handling tensorflow dataset input"""

    def __init__(self, data: _DataSourceDataTypeT, settings: DataSourceSettings):
        super().__init__(data, settings)
        self._dataset = self.data

    def process_data(self):
        self._transform_tf_dataset()

    def initialize_probs_df(self) -> DataFrame:
        return DataFrame({ObjectClassificationConstants.LABELS_COL_NAME: self.get_labels()})

    def _get_binary_labels(self):
        labels = self._extract_labels()
        return labels

    def _get_multiclass_labels(self):
        return self._extract_labels()
