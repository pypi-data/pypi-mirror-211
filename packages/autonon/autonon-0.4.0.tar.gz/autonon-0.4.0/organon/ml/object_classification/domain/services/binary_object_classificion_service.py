"""Includes BinaryObjectClassificationService"""
from typing import Tuple, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd
from organon.ml.object_classification.common.object_classification_constants import ObjectClassificationConstants
from organon.ml.object_classification.domain.data_sources.tf_dataset_data_source_handler import \
    TfDatasetDataSourceHandler
from organon.ml.object_classification.domain.services.base_object_classification_service import \
    BaseObjectClassificationService

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class BinaryObjectClassificationService(BaseObjectClassificationService):
    """Class for Binary Object Classification"""

    def _create_final_dense_layer(self, base_model: "tf.Tensor", inputs: "tf.keras.Input",
                                  layer_num: int) -> "tf.keras.Model":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        base_model = self._add_final_base_layers(base_model)
        outputs = self._get_output_layer(base_model, 1)
        return tf.keras.Model(inputs, outputs)

    def _get_output_layer(self, base_model: "tf.Tensor", layer_num: int) -> "tf.keras.layers.Dense":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        return tf.keras.layers.Dense(layer_num)(base_model)

    def _get_compiled_model(self, fine_tuning: bool = False) -> "tf.keras.Model":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        return self.model.compile(optimizer=self._get_optimizer(fine_tuning=fine_tuning),
                                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                                  metrics=tf.keras.metrics.BinaryAccuracy())

    def _generate_image_data(self) -> Tuple[TfDatasetDataSourceHandler, TfDatasetDataSourceHandler]:
        return self._generate_train_validation_data(label_mode="binary")

    def _get_avg_parameter(self, average: Optional[str]) -> str:
        return "binary" if average is None else average

    def _get_predictions(self, probs: np.ndarray) -> np.ndarray:
        return np.where(probs > self._settings.prediction_threshold, 1, 0)

    def _set_probas(self, probs_df: pd.DataFrame, probs: np.ndarray) -> pd.DataFrame:
        probs_df.loc[:, ObjectClassificationConstants.PROBA_COL_NAME] = probs.flatten()
        return probs_df
