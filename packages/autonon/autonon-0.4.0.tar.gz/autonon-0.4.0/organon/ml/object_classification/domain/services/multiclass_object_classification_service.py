"""Incldues MulticlassObjectClassificationService"""
from typing import Tuple, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.object_classification.common.object_classification_constants import ObjectClassificationConstants
from organon.ml.object_classification.domain.data_sources.tf_dataset_data_source_handler import \
    TfDatasetDataSourceHandler
from organon.ml.object_classification.domain.services.base_object_classification_service import \
    BaseObjectClassificationService

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class MulticlassObjectClassificationService(BaseObjectClassificationService):
    """Class for Multiclass Object Classification"""

    def _get_output_layer(self, base_model: "tf.Tensor", layer_num: int) -> "tf.keras.layers.Dense":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        return tf.keras.layers.Dense(layer_num, activation="softmax")(base_model)

    def _get_compiled_model(self, fine_tuning: bool = False) -> "tf.keras.Model":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        return self.model.compile(optimizer=self._get_optimizer(fine_tuning=fine_tuning),
                                  loss=tf.keras.losses.CategoricalCrossentropy(),
                                  metrics=tf.keras.metrics.CategoricalAccuracy())

    def _create_final_dense_layer(self, base_model: "tf.Tensor", inputs: "tf.keras.Input",
                                  layer_num: int) -> "tf.keras.Model":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        base_model = self._add_final_base_layers(base_model)
        outputs = self._get_output_layer(base_model, layer_num)
        return tf.keras.Model(inputs, outputs)

    def _generate_image_data(self) -> Tuple[TfDatasetDataSourceHandler, TfDatasetDataSourceHandler]:
        return self._generate_train_validation_data(label_mode="categorical")

    def _get_avg_parameter(self, average: Optional[str]) -> str:
        if average == "binary":
            LogHelper.warning(
                f"{average} can't be used while multiclass classification. Switching to average=\"weighted\"")
            average = "weighted"
        return "weighted" if average is None else average

    def _get_predictions(self, probs: np.ndarray) -> np.ndarray:
        return np.argmax(probs, axis=1).astype(np.uint8)

    def _set_probas(self, probs_df: pd.DataFrame, probs: np.ndarray) -> pd.DataFrame:
        for i in range(probs.shape[1]):
            probs_df.loc[:, f"{ObjectClassificationConstants.PROBA_COL_NAME}_{i}"] = probs[:, i]
        return probs_df
