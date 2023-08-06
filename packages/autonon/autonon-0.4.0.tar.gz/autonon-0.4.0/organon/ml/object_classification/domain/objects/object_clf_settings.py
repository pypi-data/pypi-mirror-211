"""Includes ObjectClfSettings class"""
from typing import Tuple

from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.common.enums.color_type import ColorType
from organon.ml.object_classification.domain.objects.fine_tuning_settings import FineTuningSettings
from organon.ml.object_classification.domain.objects.pretrained_model_settings import PretrainedModelSettings
from organon.ml.object_classification.domain.objects.transfer_learning_settings import TransferLearningSettings
from organon.ml.object_classification.domain.objects.data_augmentation_settings import DataAugmentationSettings


class ObjectClfSettings:
    """Settings for object classification"""

    def __init__(self, train_data_dir: str,
                 pretrained_model_settings: PretrainedModelSettings = None,
                 transfer_learning_settings: TransferLearningSettings = None,
                 fine_tuning_settings: FineTuningSettings = None,
                 data_augmentation_settings: DataAugmentationSettings = None,
                 validation_data_dir: str = None,
                 validation_data_ratio: float = 0.2, image_size: Tuple[int, int] = (150, 150),
                 batch_size: int = 50, prediction_threshold: float = 0, color_mode: ColorType = ColorType.RGB,
                 random_seed: int = 42):
        # pylint: disable=too-many-arguments
        self.train_data_dir: str = train_data_dir
        self.validation_data_dir: str = validation_data_dir
        self.clf_mode: ClassificationType = None
        self.color_mode: ColorType = color_mode
        self.validation_data_ratio: float = validation_data_ratio
        self.image_size: Tuple[int, int] = image_size
        self.batch_size: int = batch_size
        self.pretrained_model_settings = pretrained_model_settings if pretrained_model_settings is not None \
            else PretrainedModelSettings()
        self.transfer_learning_settings = transfer_learning_settings if transfer_learning_settings is not None \
            else TransferLearningSettings()
        self.data_augmentation_settings = data_augmentation_settings
        self.fine_tuning_settings = fine_tuning_settings
        self.prediction_threshold = prediction_threshold
        self.random_seed: int = random_seed
