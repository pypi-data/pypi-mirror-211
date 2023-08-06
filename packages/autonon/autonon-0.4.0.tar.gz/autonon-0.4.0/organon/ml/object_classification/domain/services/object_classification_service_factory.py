"""Includes ObjectClassificationServiceFactory class"""
import os
from typing import Union

from organon.fl.core.fileoperations import directory_helper
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.object_classification.common.helpers import throw_val_ex_with_log
from organon.ml.object_classification.domain.objects.object_clf_settings import \
    ObjectClfSettings
from organon.ml.object_classification.domain.services.binary_object_classificion_service import \
    BinaryObjectClassificationService
from organon.ml.object_classification.domain.services.multiclass_object_classification_service import \
    MulticlassObjectClassificationService


class ObjectClassificationServiceFactory:
    """Class for deciding which service is going to be used in object classification (Binary-Multiclass)"""
    @staticmethod
    def get_classification_service(settings: ObjectClfSettings) -> Union[
            BinaryObjectClassificationService, MulticlassObjectClassificationService]:
        """Returns proper service"""
        train_dir = settings.train_data_dir
        if not directory_helper.exists(train_dir):
            return throw_val_ex_with_log(f"Directory: {train_dir} not found!")

        n_of_classes = len(os.listdir(train_dir))
        if n_of_classes == 2:
            LogHelper.info("Binary classification will start")
            settings.clf_mode = ClassificationType.BINARY
            return BinaryObjectClassificationService(settings)
        if n_of_classes > 2:
            settings.clf_mode = ClassificationType.MULTICLASS
            LogHelper.info("Categorical classification will start")
            return MulticlassObjectClassificationService(settings)
        return throw_val_ex_with_log("At least 2 classes are required for classification!")
