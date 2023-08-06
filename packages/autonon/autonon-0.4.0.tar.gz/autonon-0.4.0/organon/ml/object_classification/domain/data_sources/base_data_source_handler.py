"""Includes BaseDataSourceHandler class"""
import abc
from typing import TypeVar, Generic, TYPE_CHECKING

import numpy as np
import pandas as pd

from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.object_classification.common.helpers import throw_val_ex_with_log
from organon.ml.object_classification.domain.objects.data_source_settings import DataSourceSettings

_DataSourceDataTypeT = TypeVar("_DataSourceDataTypeT")

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class BaseDataSourceHandler(Generic[_DataSourceDataTypeT], metaclass=abc.ABCMeta):
    """Class for handling data different types of data input and outputs"""

    def __init__(self, data: _DataSourceDataTypeT, settings: DataSourceSettings):
        self.data: _DataSourceDataTypeT = data
        self.settings: DataSourceSettings = settings
        self._dataset: "tf.data.Dataset" = None

    @property
    def dataset(self):
        """dataset attribute property method"""
        return self._dataset

    def get_labels(self):
        """Get labels from tensorflow dataset"""
        if self.settings.clf_type == ClassificationType.BINARY:
            return self._get_binary_labels()
        if self.settings.clf_type == ClassificationType.MULTICLASS:
            return self._get_multiclass_labels()
        return throw_val_ex_with_log("Classification type is ambiguous!")

    @abc.abstractmethod
    def process_data(self):
        """Load and transform data"""
        raise NotImplementedError

    @abc.abstractmethod
    def initialize_probs_df(self) -> pd.DataFrame:
        """Initialize probs_df with proper columns"""
        raise NotImplementedError

    @abc.abstractmethod
    def _get_binary_labels(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_multiclass_labels(self):
        raise NotImplementedError

    def _extract_labels(self):
        return np.array([y for _, y in self.dataset])

    def _transform_tf_dataset(self):
        import tensorflow as tf # pylint: disable=import-outside-toplevel

        def transform(image, label):
            image = tf.image.convert_image_dtype(image, tf.float32)
            image = tf.image.resize_with_pad(image, target_height=self.settings.image_size[1],
                                             target_width=self.settings.image_size[0])
            image = tf.expand_dims(image, axis=0)
            return image, label

        self._dataset = self._dataset.map(transform)
