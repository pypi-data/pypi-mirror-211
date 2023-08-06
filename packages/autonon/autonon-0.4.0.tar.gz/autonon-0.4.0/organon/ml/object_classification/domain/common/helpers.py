"""Includes common methods in object classification domain"""
from organon.ml.object_classification.domain.objects.data_source_settings import DataSourceSettings
from organon.ml.object_classification.domain.objects.object_clf_settings import ObjectClfSettings


def get_data_source_settings(obj_clf_settings: ObjectClfSettings) -> DataSourceSettings:
    """Returns data source settings object for given Object Classification Settings"""
    return DataSourceSettings(obj_clf_settings.clf_mode, obj_clf_settings.validation_data_ratio,
                              obj_clf_settings.image_size, obj_clf_settings.batch_size, obj_clf_settings.color_mode,
                              obj_clf_settings.random_seed)
