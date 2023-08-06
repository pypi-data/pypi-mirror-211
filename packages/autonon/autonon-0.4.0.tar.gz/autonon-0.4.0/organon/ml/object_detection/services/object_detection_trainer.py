"""Includes ObjectDetectionTrainer class"""
import os
import urllib

import numpy as np
import yaml

from organon.fl.core.exceptionhandling.known_exception import KnownException
from organon.fl.core.fileoperations import directory_helper
from organon.fl.core.helpers import guid_helper
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.object_detection.domain.object_detection_training_service import ObjectDetectionTrainingService
from organon.ml.object_detection.services.enums.map_metric import MapMetrics
from organon.ml.object_detection.services.enums.model_type import ModelTypes


class ObjectDetectionTrainer:
    """Class for training ObjectDetection models"""

    def __init__(self, pretrained_model_path: str, yaml_data_dir: str, batch_size: int = 16,
                 epochs: int = 100, map_metric: str = 'map50', map_threshold: float = 0.8):
        map_metric = get_enum(map_metric.upper(), MapMetrics)

        self._service: ObjectDetectionTrainingService = None
        self._yaml_data_dir = yaml_data_dir
        self._pretrained_model_path = pretrained_model_path
        self._batch_size = batch_size
        self._epochs = epochs
        self._is_trained_on_full_data = False
        self._map_metric: MapMetrics = map_metric
        self._map_threshold: float = map_threshold

    def train(self, sampling: bool = False, sampling_ratio: float = 0.3, random_seed: int = 42,
              output_folder: str = None, override_data_files: bool = False):
        """
        Runs training
        :param sampling: If True, training will be done on a sample of the train data.
            If best mAP value among models created during this training is higher than
            pre_train_eval_min_map(see set_pre_train_settings method), training on full data will not run. Else,
            training will run again on full data
        :param sampling_ratio:
        :param random_seed:
        :param output_folder:
        :param override_data_files:
        """

        if output_folder is None:
            output_folder = os.path.dirname(self._yaml_data_dir)

        if not directory_helper.exists(output_folder):
            raise ValueError(f"Directory '{output_folder}' does not exist")
        train_on_full_data_flag = True
        # pylint: disable=too-many-arguments
        if sampling:
            LogHelper.warning("Training with sample data started")
            new_yaml_dir = None
            try:
                new_yaml_dir = self._generate_new_data_dir_for_pre_train(sampling_ratio, random_seed)

                pre_train_service = ObjectDetectionTrainingService(new_yaml_dir,
                                                                   self._pretrained_model_path)
                pre_train_service.train(batch_size=self._batch_size, epochs=self._epochs, random_seed=random_seed,
                                        output_folder=output_folder, override_data_files=override_data_files)

                map_score = pre_train_service.evaluate(self._map_metric)
                if map_score > self._map_threshold:
                    train_on_full_data_flag = False
                    LogHelper.warning(
                        f"map score is {map_score} which is greater than the threshold {self._map_threshold}."
                        "Training on full data step will be skipped.")
                    self._service = pre_train_service
                    self._is_trained_on_full_data = train_on_full_data_flag
                    return
                directory_helper.delete_directory_with_contents(os.path.dirname(new_yaml_dir))

            except Exception as exc:
                LogHelper.error("Error occurred while pre-training")
                if new_yaml_dir:
                    LogHelper.info("Cleaning data directory generated for pre-training")
                    directory_helper.delete_directory_with_contents(os.path.dirname(new_yaml_dir))

                raise exc

        try:
            if train_on_full_data_flag:
                service = ObjectDetectionTrainingService(self._yaml_data_dir, self._pretrained_model_path)
                LogHelper.info("Training with full data started")
                service.train(batch_size=self._batch_size, epochs=self._epochs, random_seed=random_seed,
                              output_folder=output_folder, override_data_files= override_data_files)
                self._service = service
                self._is_trained_on_full_data = train_on_full_data_flag
        except Exception as exc:
            msg = "Error occurred while training on full data."
            raise Exception(msg) from exc

    @property
    def is_trained_on_full_data(self):
        """Returns if the model is trained on full data, not pretrain data"""
        return self._is_trained_on_full_data

    @classmethod
    def load_pretrained_model_from_web(cls, target_path: str,
                                       model_type: str = "small"):
        """Loads a pretrained model to given file path after downloading from web. The default model to be downloaded is
        'YOLOv8s' and its approx 25 MB
        :param target_path: File path to download the pretrained model in
        :param model_type: Model type keyword to be downloaded
        """
        model_type_enum = get_enum(model_type.upper(), ModelTypes)
        model_url = ObjectDetectionTrainer._get_model_by_model_type(model_type_enum)

        if os.path.isfile(target_path):
            raise FileExistsError(f"File '{target_path}' already exists")
        try:
            LogHelper.warning(f"Started loading pretrained model from '{model_url}'")
            urllib.request.urlretrieve(model_url, target_path)  # nosec
        except Exception as exc:
            msg = "Error occurred while loading a pretrained model from internet"
            raise Exception(msg) from exc
        LogHelper.warning(f"Pretrained model loaded to file {target_path}")

    def _generate_new_data_dir_for_pre_train(self, data_sampling_ratio: float, random_seed: int):
        guid = guid_helper.new_guid(8)
        try:
            new_data_dir = os.path.join(os.path.dirname(self._yaml_data_dir),
                                        f"sample_{guid}")
            LogHelper.info(f"Generating new data directory for pre training in {new_data_dir}")
            directory_helper.create(new_data_dir, exception_if_exists=True)
            original_train_image_dir = ObjectDetectionTrainingService.get_train_images_dir_path_yaml(
                self._yaml_data_dir)
            original_train_labels_dir = ObjectDetectionTrainingService.get_train_label_dir_path_yaml(
                self._yaml_data_dir)
            valid_image_files_dir = ObjectDetectionTrainingService.get_validation_images_dir_path_yaml(
                self._yaml_data_dir)
            valid_labels_dir = ObjectDetectionTrainingService.get_validation_label_dir_path_yaml(self._yaml_data_dir)

            train_image_files, train_label_files = self._get_sampled_image_files(original_train_image_dir,
                                                                                 original_train_labels_dir,
                                                                                 data_sampling_ratio, random_seed)
            valid_image_files, val_label_files = self._get_sampled_image_files(valid_image_files_dir, valid_labels_dir,
                                                                               data_sampling_ratio, random_seed)

            new_train_images_dir = ObjectDetectionTrainingService.get_train_images_dir_path(new_data_dir)
            new_train_labels_dir = ObjectDetectionTrainingService.get_train_label_dir_path(new_data_dir)
            new_valid_images_dir = ObjectDetectionTrainingService.get_validation_images_dir_path(new_data_dir)
            new_valid_labels_dir = ObjectDetectionTrainingService.get_validation_label_dir_path(new_data_dir)

            new_yaml_dir = ObjectDetectionTrainer. \
                _create_updated_yaml_file_with_new_data_locations(self._yaml_data_dir,
                                                                  new_data_dir,
                                                                  new_train_images_dir,
                                                                  new_valid_images_dir)

            LogHelper.info(f"Copying sampled train images for pre training in {new_train_images_dir}")
            directory_helper.copy_files(train_image_files, new_train_images_dir)
            LogHelper.info(f"Copying sampled validation images for pre training in {new_valid_images_dir}")
            directory_helper.copy_files(valid_image_files, new_valid_images_dir)
            LogHelper.info(f"Copying sampled validation labels for pre training in {new_valid_labels_dir}")
            directory_helper.copy_files(val_label_files, new_valid_labels_dir)
            LogHelper.info(f"Copying sampled train images for pre training in {new_train_labels_dir}")
            directory_helper.copy_files(train_label_files, new_train_labels_dir)
        except KnownException as k_exc:
            raise k_exc
        except ValueError as v_exc:
            raise v_exc
        except Exception as exc:
            msg = "Error occurred while generating new data dirs for sampling."
            raise Exception(msg) from exc

        return new_yaml_dir

    @staticmethod
    def _get_sampled_image_files(original_image_files_dir: str, original_label_files_dir: str,
                                 data_sampling_ratio: float, random_seed: int):
        all_file_names = os.listdir(original_image_files_dir)
        num_files_to_get = int(len(all_file_names) * data_sampling_ratio)
        if num_files_to_get == 0:
            raise KnownException("Not enough files to run pre-evaluation, "
                                 "try increasing pre_train_eval_data_sampling_ratio or disable pre evaluation "
                                 "to run training directly with full data")
        np.random.seed(random_seed)
        files = np.random.choice(all_file_names, num_files_to_get, replace=False)
        image_files = [os.path.join(original_image_files_dir, file) for file in files]
        label_files = [os.path.join(original_label_files_dir,
                                    f"{os.path.splitext(os.path.basename(file))[0]}.txt") for file in image_files]

        return image_files, label_files

    @staticmethod
    def _create_updated_yaml_file_with_new_data_locations(yaml_file_location, new_data_dir, new_train_dir, new_val_dir):

        yaml_dir, yaml_filename = os.path.split(yaml_file_location)

        updated_yaml_filename = yaml_filename.replace('.yaml', '_updated.yaml')

        relative_path = os.path.relpath(new_data_dir, yaml_dir)
        updated_yaml_dir = os.path.join(yaml_dir, relative_path)

        updated_yaml_file_location = os.path.join(updated_yaml_dir, updated_yaml_filename)

        os.makedirs(updated_yaml_dir, exist_ok=True)

        with open(yaml_file_location, encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)

        updated_yaml_data = yaml_data.copy()
        updated_yaml_data['train'] = new_train_dir
        updated_yaml_data['val'] = new_val_dir

        with open(updated_yaml_file_location, 'w', encoding="utf-8") as file:
            yaml.dump(updated_yaml_data, file)

        return updated_yaml_file_location

    @staticmethod
    def _get_model_by_model_type(model_type: ModelTypes):
        """return the model url from given model keyword"""

        if model_type == ModelTypes.NANO:
            model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        elif model_type == ModelTypes.SMALL:
            model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt"
        elif model_type == ModelTypes.MEDIUM:
            model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt"
        elif model_type == ModelTypes.LARGE:
            model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt"
        elif model_type == ModelTypes.XLARGE:
            model_url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt"
        else:
            raise ValueError("Wrong Model Type keyword. Model Types can only be nano, small, medium, large and Xlarge")
        return model_url
