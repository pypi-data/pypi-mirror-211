"""Includes ObjectClfSettingsValidator class"""
from typing import Tuple

from organon.ml.common.enums.pretrained_model_type import PretrainedModelType
from organon.ml.object_classification.common.helpers import check_directory, throw_val_ex_with_log
from organon.ml.object_classification.common.object_classification_constants import ObjectClassificationConstants
from organon.ml.object_classification.domain.objects.object_clf_settings import ObjectClfSettings


class ObjectClfSettingsValidator:
    """Class for validating ObjectClfSettings"""

    @staticmethod
    def check_settings(settings: ObjectClfSettings):
        """Check directories and image sizes"""
        check_directory(settings.train_data_dir)
        if settings.validation_data_dir is not None:
            check_directory(settings.validation_data_dir)
        ObjectClfSettingsValidator._check_image_size(settings.pretrained_model_settings.model, settings.image_size)

    @staticmethod
    def _check_image_size(model: PretrainedModelType, image_size: Tuple[int, int]):
        size_error = "Using {} model, image_size (width, height) should be bigger than {}"
        err = None
        if model == PretrainedModelType.XCEPTION and (
                image_size[
                    0] <= ObjectClassificationConstants.XCEPTION_MIN_IMG_SIZE or
                image_size[
                    1] <= ObjectClassificationConstants.XCEPTION_MIN_IMG_SIZE):
            err = size_error.format(PretrainedModelType.XCEPTION.name,
                                    ObjectClassificationConstants.XCEPTION_MIN_IMG_SIZE)

        elif model == PretrainedModelType.RES_NET_50_V2 and (
                image_size[
                    0] <= ObjectClassificationConstants.RES_NET_50_V2_MIN_IMG_SIZE or
                image_size[
                    1] <= ObjectClassificationConstants.RES_NET_50_V2_MIN_IMG_SIZE):
            err = size_error.format(PretrainedModelType.RES_NET_50_V2.name,
                                    ObjectClassificationConstants.RES_NET_50_V2_MIN_IMG_SIZE)

        elif model == PretrainedModelType.INCEPTION_RES_NET_V2 and (
                image_size[
                    0] <= ObjectClassificationConstants.INCEPTION_RES_NET_V2_MIN_IMG_SIZE or
                image_size[
                    1] <= ObjectClassificationConstants.INCEPTION_RES_NET_V2_MIN_IMG_SIZE):
            err = size_error.format(PretrainedModelType.INCEPTION_RES_NET_V2.name,
                                    ObjectClassificationConstants.INCEPTION_RES_NET_V2_MIN_IMG_SIZE)
        if err:
            throw_val_ex_with_log(err)
