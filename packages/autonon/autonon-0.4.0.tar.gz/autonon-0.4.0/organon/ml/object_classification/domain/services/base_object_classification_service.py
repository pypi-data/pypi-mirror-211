"""Includes BaseObjectClassificationService"""
import abc
import math
import os
from typing import Dict, List, Optional, Tuple, Union, TYPE_CHECKING

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.utils import class_weight

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.common.enums.color_type import ColorType
from organon.ml.common.enums.optimizer_type import OptimizerType
from organon.ml.object_classification.common.helpers import throw_val_ex_with_log
from organon.ml.object_classification.domain.common.helpers import get_data_source_settings
from organon.ml.object_classification.domain.common.object_clf_settings_validator import ObjectClfSettingsValidator
from organon.ml.object_classification.common.object_classification_constants import ObjectClassificationConstants
from organon.ml.object_classification.domain.data_sources.base_data_source_handler import BaseDataSourceHandler
from organon.ml.object_classification.domain.data_sources.data_source_handler_factory import DataSourceHandlerFactory
from organon.ml.object_classification.domain.data_sources.tf_dataset_data_source_handler import \
    TfDatasetDataSourceHandler
from organon.ml.object_classification.domain.data_sources.unlabeled_dir_data_source_handler import \
    UnlabeledDirDataSourceHandler
from organon.ml.object_classification.domain.objects.object_clf_settings import \
    ObjectClfSettings
from organon.ml.object_classification.domain.common.base_model_generator import BaseModelGenerator

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class BaseObjectClassificationService(metaclass=abc.ABCMeta):
    """Base Object classification service"""

    def __init__(self, settings: ObjectClfSettings):
        self._settings = settings
        self.model: "tf.keras.Model" = None

    def fit(self):
        """Fit classifier"""

        ObjectClfSettingsValidator.check_settings(self._settings)

        class_names = os.listdir(self._settings.train_data_dir)

        LogHelper.info("Reading train data..")
        train_data, validation_data = self._generate_image_data()

        class_weights = self._check_class_weights(class_names, train_data)

        LogHelper.info("Preparing model..")
        base_model, inputs = BaseModelGenerator.get_base_model(self._settings.image_size,
                                                               self._settings.color_mode,
                                                               self._settings.pretrained_model_settings,
                                                               self._settings.data_augmentation_settings,
                                                               self._settings.random_seed)

        self.model = self._create_final_dense_layer(base_model, inputs, layer_num=len(class_names))

        LogHelper.info("Model training started..")
        self._train_model(train_data, validation_data, class_weights, base_model)

        if self._settings.fine_tuning_settings is not None:
            LogHelper.info("Fine tuning started..")
            self._train_model(train_data, validation_data, class_weights, base_model, fine_tuning=True)

    def evaluate(self, data: Union["tf.data.Dataset", str], average: str = None, return_df: bool = True,
                 is_processed: bool = False) -> Tuple[Dict[str, float], Optional[pd.DataFrame]]:
        """Predict and evaluate predictions"""

        data_source = DataSourceHandlerFactory.get_data_source_handler(data, self._settings)
        if isinstance(data_source, UnlabeledDirDataSourceHandler):
            msg = "Unlabeled sources can't be evaluated!"
            LogHelper.error(msg)
            raise TypeError(msg)

        probs_df = self.predict(data, is_processed)

        y_true = probs_df.loc[:, ObjectClassificationConstants.LABELS_COL_NAME]
        y_pred = pd.to_numeric(probs_df.loc[:, ObjectClassificationConstants.PREDICTON_COL_NAME])

        average = self._get_avg_parameter(average)

        metrics = {"accuracy": accuracy_score(y_true, y_pred),
                   "recall": recall_score(y_true, y_pred, average=average),
                   "f1": f1_score(y_true, y_pred, average=average),
                   "precision": precision_score(y_true, y_pred, average=average)}
        return (metrics, probs_df) if return_df else (metrics, None)

    def predict(self, data: Union["tf.data.Dataset", str], is_processed: bool = False) -> pd.DataFrame:
        """Predict object in image"""

        data_source = DataSourceHandlerFactory.get_data_source_handler(data, self._settings)

        probs = self._get_probs(data_source, is_processed)

        predictions = self._get_predictions(probs)

        pred_df = data_source.initialize_probs_df()
        pred_df[ObjectClassificationConstants.PREDICTON_COL_NAME] = predictions

        return pred_df

    def predict_proba(self, data: Union["tf.data.Dataset", str], is_processed: bool = False) -> pd.DataFrame:
        """Predict probabilities of object in image"""

        data_source = DataSourceHandlerFactory.get_data_source_handler(data, self._settings)

        probs = self._get_probs(data_source, is_processed)

        probs_df: pd.DataFrame = data_source.initialize_probs_df()

        probs_df = self._set_probas(probs_df, probs)

        return probs_df

    def get_processed_data(self, data: Union["tf.data.Dataset", str]) -> "tf.data.Dataset":
        """Convert data into a format the model can predict"""
        data_source = DataSourceHandlerFactory.get_data_source_handler(data, self._settings)
        data_source.process_data()
        return data_source.dataset

    @abc.abstractmethod
    def _set_probas(self, probs_df: pd.DataFrame, probs: np.ndarray) -> pd.DataFrame:
        raise NotImplementedError

    @abc.abstractmethod
    def _create_final_dense_layer(self, base_model: "tf.Tensor", inputs: "tf.keras.Input",
                                  layer_num: int) -> "tf.keras.Model":
        raise NotImplementedError

    @abc.abstractmethod
    def _get_predictions(self, probs: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_avg_parameter(self, average: Optional[str]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_compiled_model(self, fine_tuning: bool = False) -> "tf.keras.Model":
        raise NotImplementedError

    @abc.abstractmethod
    def _get_output_layer(self, base_model: "tf.Tensor", layer_num: int):
        raise NotImplementedError

    @abc.abstractmethod
    def _generate_image_data(self):
        raise NotImplementedError

    def _get_probs(self, data: BaseDataSourceHandler, is_processed: bool = False) -> np.ndarray:

        if not is_processed:
            LogHelper.info("Data is not preprocessed! Processing data...")
            data.process_data()

        return self.model.predict(data.dataset)

    def _get_color_parameter(self) -> str:
        if self._settings.color_mode == ColorType.RGB:
            color_mode = "rgb"
        elif self._settings.color_mode == ColorType.RGBA:
            color_mode = "rgba"
        elif self._settings.color_mode == ColorType.GRAY:
            color_mode = "grayscale"
        else:
            return throw_val_ex_with_log("Color type is ambiguous!")

        return color_mode

    def _get_optimizer(self, fine_tuning: bool = False) -> "tf.keras.optimizers":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        opt = self._settings.fine_tuning_settings.optimizer if fine_tuning \
            else self._settings.transfer_learning_settings.optimizer
        learning_rate = self._get_learning_rate(opt, fine_tuning)
        if opt == OptimizerType.ADAM:
            optimizer = tf.keras.optimizers.Adam(learning_rate)
        elif opt == OptimizerType.ADADELTA:
            optimizer = tf.keras.optimizers.Adadelta(learning_rate)
        elif opt == OptimizerType.ADAGRAD:
            optimizer = tf.keras.optimizers.Adagrad(learning_rate)
        elif opt == OptimizerType.ADAMAX:
            optimizer = tf.keras.optimizers.Adamax(learning_rate)
        elif opt == OptimizerType.FTRL:
            optimizer = tf.keras.optimizers.Ftrl(learning_rate)
        elif opt == OptimizerType.NADAM:
            optimizer = tf.keras.optimizers.Nadam(learning_rate)
        elif opt == OptimizerType.SGD:
            optimizer = tf.keras.optimizers.SGD(learning_rate)
        elif opt == OptimizerType.RMSPROP:
            optimizer = tf.keras.optimizers.RMSprop(learning_rate)
        else:
            return throw_val_ex_with_log("Optimizer is ambiguous!")

        return optimizer

    def _get_learning_rate(self, opt: OptimizerType, fine_tuning: bool = False) -> float:
        learning_rate = self._settings.fine_tuning_settings.learning_rate if fine_tuning \
            else self._settings.transfer_learning_settings.learning_rate

        if opt == OptimizerType.SGD:
            if not fine_tuning and self._settings.transfer_learning_settings.learning_rate == 0.001:
                learning_rate = 0.01
        return learning_rate

    def _get_steps_parameter(self, data: "tf.data.Dataset") -> int:
        return math.ceil(int(data.cardinality().numpy() // self._settings.batch_size)) - 1

    def _train_model(self, train_data: TfDatasetDataSourceHandler, validation_data: TfDatasetDataSourceHandler,
                     class_weights: Optional[Dict[int, float]], base_model: "tf.Tensor", fine_tuning: bool = False):
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                patience=self._settings.fine_tuning_settings.early_stopping_patience if fine_tuning
                else self._settings.transfer_learning_settings.early_stopping),
            tf.keras.callbacks.TensorBoard()
        ]

        if fine_tuning:
            base_model.trainable = True

        self._get_compiled_model(fine_tuning)

        epochs = self._settings.fine_tuning_settings.epoch if fine_tuning \
            else self._settings.transfer_learning_settings.epoch

        self.model.fit(
            x=train_data.data,
            epochs=epochs,
            steps_per_epoch=self._get_steps_parameter(train_data.data),
            validation_data=validation_data.data,
            validation_steps=self._get_steps_parameter(validation_data.data),
            class_weight=class_weights,
            callbacks=callbacks)

    def _add_final_base_layers(self, base_model: "tf.Tensor") -> "tf.Tensor":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        base_model = tf.keras.layers.GlobalAveragePooling2D()(base_model)
        base_model = tf.keras.layers.Dropout(self._settings.transfer_learning_settings.dropout)(base_model)
        return base_model

    def _generate_train_validation_data(self, label_mode: str) -> Tuple[
        TfDatasetDataSourceHandler, TfDatasetDataSourceHandler]:
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        if self._settings.validation_data_dir is not None:
            train_data = tf.keras.utils.image_dataset_from_directory(directory=self._settings.train_data_dir,
                                                                     batch_size=self._settings.batch_size,
                                                                     image_size=self._settings.image_size,
                                                                     shuffle=True,
                                                                     seed=self._settings.random_seed,
                                                                     color_mode=self._get_color_parameter(),
                                                                     label_mode=label_mode)

            validation_data = tf.keras.utils.image_dataset_from_directory(
                directory=self._settings.validation_data_dir,
                batch_size=self._settings.batch_size,
                image_size=self._settings.image_size,
                shuffle=False, seed=self._settings.random_seed,
                color_mode=self._get_color_parameter(),
                label_mode=label_mode)

        else:
            train_data, validation_data = tf.keras.utils.image_dataset_from_directory(
                directory=self._settings.train_data_dir,
                batch_size=self._settings.batch_size,
                image_size=self._settings.image_size,
                shuffle=True, seed=self._settings.random_seed,
                validation_split=self._settings.validation_data_ratio,
                subset="both", color_mode=self._get_color_parameter(), label_mode=label_mode)

        settings = get_data_source_settings(self._settings)

        return TfDatasetDataSourceHandler(train_data, settings), TfDatasetDataSourceHandler(validation_data, settings)

    def _check_class_weights(self, class_names: List[str], train_data: TfDatasetDataSourceHandler) -> Optional[
        Dict[int, float]]:

        class_dirs = [os.path.join(self._settings.train_data_dir, class_name) for class_name in class_names]

        n_of_samples = [len(os.listdir(directory)) for directory in class_dirs]

        n_of_total_samples = sum(n_of_samples)
        if n_of_total_samples < self._settings.batch_size:
            throw_val_ex_with_log(
                f"Batch size ({self._settings.batch_size}) can't be bigger than "
                f"total sample number ({n_of_total_samples})")

        labels = np.concatenate(train_data.get_labels(), axis=0)
        labels = labels.flatten() if self._settings.clf_mode == ClassificationType.BINARY else np.argmax(labels, axis=1)

        for (label, class_name, sample_number) in zip(labels, class_names, n_of_samples):
            LogHelper.info(f"Class {label}: {class_name}, {sample_number} samples")

        if len(set(n_of_samples)) != 1:
            LogHelper.info("Dataset is inbalanced")
            class_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                              classes=np.unique(labels),
                                                              y=labels)
            return dict(enumerate(class_weights))
        return None
