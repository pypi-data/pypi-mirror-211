"""Includes ObjectClassifier class."""
from typing import Optional, Tuple, Union, Dict, TYPE_CHECKING
from pandas import DataFrame

from organon.ml.common.enums.color_type import ColorType
from organon.ml.common.enums.optimizer_type import OptimizerType
from organon.ml.common.enums.pretrained_model_type import PretrainedModelType
from organon.ml.common.enums.random_flip_type import RandomFlipType
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.object_classification.domain.objects.data_augmentation_settings import DataAugmentationSettings
from organon.ml.object_classification.domain.objects.fine_tuning_settings import FineTuningSettings
from organon.ml.object_classification.domain.objects.object_clf_settings import ObjectClfSettings
from organon.ml.object_classification.domain.objects.pretrained_model_settings import PretrainedModelSettings
from organon.ml.object_classification.domain.objects.transfer_learning_settings import TransferLearningSettings
from organon.ml.object_classification.domain.services.binary_object_classificion_service import \
    BinaryObjectClassificationService
from organon.ml.object_classification.domain.services.multiclass_object_classification_service import \
    MulticlassObjectClassificationService
from organon.ml.object_classification.domain.services.object_classification_service_factory import \
    ObjectClassificationServiceFactory

if TYPE_CHECKING:
    import tensorflow as tf


class ObjectClassifier:
    """Image object classifier"""

    def __init__(self, train_data_dir: str, validation_data_dir: str = None,
                 validation_data_ratio: float = 0.2, image_size: Tuple[int, int] = (150, 150),
                 batch_size: int = 50, color_mode: str = ColorType.RGB.name, random_seed: int = 42):
        # pylint: disable=too-many-arguments
        color_mode = get_enum(color_mode, ColorType)
        self._settings = ObjectClfSettings(train_data_dir, validation_data_dir=validation_data_dir,
                                           validation_data_ratio=validation_data_ratio, image_size=image_size,
                                           batch_size=batch_size, color_mode=color_mode, random_seed=random_seed)

        self._service: Union[BinaryObjectClassificationService, MulticlassObjectClassificationService] = None
        self._fine_tuning_settings: FineTuningSettings = None
        self._transfer_lrn_settings: TransferLearningSettings = None
        self._pretrained_model_settings: PretrainedModelSettings = None
        self._data_augmentation_settings: DataAugmentationSettings = None

    def fit(self):
        """Fits classifier"""
        self._set_full_settings()
        self._service = ObjectClassificationServiceFactory.get_classification_service(self._settings)
        self._service.fit()

    def predict(self, data: Union[str, "tf.data.Dataset"], is_processed: bool = False) -> DataFrame:
        """Predict object in image"""
        return self._service.predict(data, is_processed)

    def predict_proba(self, data: Union[str, "tf.data.Dataset"], is_processed: bool = False) -> DataFrame:
        """Predict probabilities for object in image"""
        return self._service.predict_proba(data, is_processed)

    def evaluate(self, data: Union["tf.data.Dataset", str], average: str = None, return_df: bool = True,
                 is_processed: bool = False) -> Tuple[
        Dict[str, float], Optional[DataFrame]]:
        """Predict and evaluate predictions"""
        return self._service.evaluate(data, is_processed=is_processed, average=average, return_df=return_df)

    def get_processed_data(self, data: Union[str, "tf.data.Dataset"]) -> "tf.data.Dataset":
        """Convert data into a format the model can predict"""
        return self._service.get_processed_data(data)

    def set_fine_tuning_settings(self, epoch: int = 10, early_stopping_patience: int = 2,
                                 early_stopping_min_delta=0.001, learning_rate: float = 1e-5,
                                 optimizer: str = OptimizerType.ADAM.name):
        """Sets fine tuning settings for fitting"""
        opt = get_enum(optimizer, OptimizerType)
        self._fine_tuning_settings = FineTuningSettings(epoch, early_stopping_patience, early_stopping_min_delta,
                                                        learning_rate, opt)

    def set_transfer_learning_settings(self, epoch: int = 20, early_stopping: int = 2,
                                       optimizer: str = OptimizerType.ADAM.name,
                                       dropout: float = 0.2, learning_rate: float = 0.001):
        """Sets transfer learning settings for fitting"""
        opt = get_enum(optimizer, OptimizerType)
        self._transfer_lrn_settings = TransferLearningSettings(epoch, early_stopping, opt, dropout, learning_rate)

    def set_pretrained_model_settings(self, model: str = PretrainedModelType.XCEPTION.name,
                                      weights: Optional[str] = "imagenet"):
        """Sets pretrained model settings for fitting"""
        model_enum_val = get_enum(model, PretrainedModelType)
        self._pretrained_model_settings = PretrainedModelSettings(model_enum_val, weights)

    def set_data_augmentation_settings(self, random_flip: str = RandomFlipType.HORIZONTAL_AND_VERTICAL.name,
                                       random_rotation: float = 0.1, random_zoom: float = 0.1):
        """Sets pretrained model settings for fitting"""
        random_flip_type = get_enum(random_flip, RandomFlipType)
        self._data_augmentation_settings = DataAugmentationSettings(random_flip_type, random_rotation, random_zoom)

    def _set_full_settings(self):
        if self._fine_tuning_settings is not None:
            self._settings.fine_tuning_settings = self._fine_tuning_settings
        if self._transfer_lrn_settings is not None:
            self._settings.transfer_learning_settings = self._transfer_lrn_settings
        if self._pretrained_model_settings is not None:
            self._settings.pretrained_model_settings = self._pretrained_model_settings
        if self._data_augmentation_settings is not None:
            self._settings.data_augmentation_settings = self._data_augmentation_settings
