"""Includes BaseModelGenerator class"""
from typing import Tuple, TYPE_CHECKING
from organon.ml.common.enums.pretrained_model_type import PretrainedModelType
from organon.ml.common.enums.color_type import ColorType
from organon.ml.common.enums.random_flip_type import RandomFlipType
from organon.ml.object_classification.common.helpers import throw_val_ex_with_log
from organon.ml.object_classification.domain.objects.data_augmentation_settings import DataAugmentationSettings
from organon.ml.object_classification.domain.objects.pretrained_model_settings import PretrainedModelSettings

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class BaseModelGenerator:
    """BaseModelGenarator class"""

    @staticmethod
    def get_base_model(image_size: Tuple[int, int], color_mode: ColorType,
                       pretrained_model_settings: PretrainedModelSettings,
                       data_augmentation_settings: DataAugmentationSettings = None, random_seed: int = 42) -> \
            Tuple["tf.Tensor", "tf.keras.Input"]:
        """Returns base_model with given settings"""
        import tensorflow as tf  # pylint: disable=import-outside-toplevel

        input_shape = image_size + BaseModelGenerator._get_input_dim(color_mode)

        inputs = tf.keras.Input(shape=input_shape)

        if data_augmentation_settings is not None:
            data_augmentation = BaseModelGenerator._get_augmentation_layers(data_augmentation_settings,
                                                                            random_seed=random_seed)
            inputs = data_augmentation(inputs)

        base_model_args = dict(weights=pretrained_model_settings.weights,
                               input_shape=input_shape, include_top=False)
        base_model_type = pretrained_model_settings.model

        if base_model_type == PretrainedModelType.XCEPTION:
            base_model = tf.keras.applications.Xception(**base_model_args)
            process_input = tf.keras.applications.xception.preprocess_input(inputs)
        elif base_model_type == PretrainedModelType.INCEPTION_RES_NET_V2:
            base_model = tf.keras.applications.InceptionResNetV2(**base_model_args)
            process_input = tf.keras.applications.inception_resnet_v2.preprocess_input(inputs)
        elif base_model_type == PretrainedModelType.RES_NET_50_V2:
            base_model = tf.keras.applications.resnet_v2.ResNet50V2(**base_model_args)
            process_input = tf.keras.applications.resnet_v2.preprocess_input(inputs)
        elif base_model_type == PretrainedModelType.EFFICIENT_NET_B4:
            base_model = tf.keras.applications.efficientnet.EfficientNetB4(**base_model_args)
            process_input = tf.keras.applications.efficientnet.preprocess_input(inputs)
        elif base_model_type == PretrainedModelType.EFFICIENT_NET_B7:
            base_model = tf.keras.applications.efficientnet.EfficientNetB7(**base_model_args)
            process_input = tf.keras.applications.efficientnet.preprocess_input(inputs)
        else:
            return throw_val_ex_with_log("Model type is not defined!")

        base_model.trainable = False

        base_model = base_model(process_input, training=False)

        return base_model, inputs

    @staticmethod
    def _get_augmentation_layers(data_augmentation_settings: DataAugmentationSettings,
                                 random_seed: int) -> "tf.keras.Sequential":
        import tensorflow as tf  # pylint: disable=import-outside-toplevel
        if data_augmentation_settings.random_flip == RandomFlipType.HORIZONTAL_AND_VERTICAL:
            random_flip_mode = "horizontal_and_vertical"
        elif data_augmentation_settings.random_flip == RandomFlipType.HORIZONTAL:
            random_flip_mode = "horizontal"
        elif data_augmentation_settings.random_flip == RandomFlipType.VERTICAL:
            random_flip_mode = "vertical"
        else:
            return throw_val_ex_with_log("Random flip mode is ambiguous")

        seed = random_seed
        return tf.keras.Sequential([
            tf.keras.layers.RandomFlip(random_flip_mode, seed=seed),
            tf.keras.layers.RandomRotation(data_augmentation_settings.random_rotation, seed=seed),
            tf.keras.layers.RandomZoom(data_augmentation_settings.random_zoom, seed=seed)])

    @staticmethod
    def _get_input_dim(color_mode: ColorType) -> tuple:
        if color_mode == ColorType.RGB:
            input_dim = (3,)
        elif color_mode == ColorType.RGBA:
            input_dim = (4,)
        elif color_mode == ColorType.GRAY:
            input_dim = (1,)
        else:
            return throw_val_ex_with_log("Color type is ambiguous!")
        return input_dim
