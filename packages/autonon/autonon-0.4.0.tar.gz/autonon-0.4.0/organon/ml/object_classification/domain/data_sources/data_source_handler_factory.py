"""Includes ObjectClassificationServiceFactory class"""
import os
from typing import Union, TYPE_CHECKING

from organon.ml.object_classification.common.helpers import throw_val_ex_with_log, check_directory
from organon.ml.object_classification.domain.common.helpers import get_data_source_settings
from organon.ml.object_classification.domain.data_sources.labeled_dir_data_source_handler import \
    LabeledDirDataSourceHandler
from organon.ml.object_classification.domain.data_sources.tf_dataset_data_source_handler import \
    TfDatasetDataSourceHandler
from organon.ml.object_classification.domain.data_sources.unlabeled_dir_data_source_handler import \
    UnlabeledDirDataSourceHandler
from organon.ml.object_classification.domain.objects.object_clf_settings import ObjectClfSettings

if TYPE_CHECKING:
    import tensorflow as tf  # noqa


class DataSourceHandlerFactory:
    """Class for deciding which service is going to be used in object classification (Binary-Multiclass)"""

    @staticmethod
    def get_data_source_handler(data: Union["tf.data.Dataset", str], settings: ObjectClfSettings) -> Union[
            LabeledDirDataSourceHandler, UnlabeledDirDataSourceHandler, TfDatasetDataSourceHandler]:
        """Returns proper data source handler for given data"""
        settings = get_data_source_settings(settings)
        if isinstance(data, str):
            check_directory(data)
            directory_types = [os.path.isfile(os.path.join(data, directory)) for directory in os.listdir(data)]
            if all(is_file is True for is_file in directory_types):
                data_source = UnlabeledDirDataSourceHandler(data, settings)
            elif all(is_file is False for is_file in directory_types):
                data_source = LabeledDirDataSourceHandler(data, settings)
            else:
                return throw_val_ex_with_log(
                    "Prediction path should contain only unlabeled images (files) or labeled images (folders)")
        else:
            data_source = TfDatasetDataSourceHandler(data, settings)

        return data_source
