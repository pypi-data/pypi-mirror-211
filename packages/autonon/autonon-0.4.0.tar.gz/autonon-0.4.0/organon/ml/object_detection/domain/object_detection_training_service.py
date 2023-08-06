"""Includes ObjectDetectionTrainer class"""
import os

import yaml

from ultralytics import YOLO

from organon.fl.core.fileoperations import directory_helper
from organon.ml.object_detection.services.enums.map_metric import MapMetrics


class ObjectDetectionTrainingService:
    """Custom YOLOv8 model trainer for object detection"""

    def __init__(self, yaml_data_dir: str, pretrained_model_path: str):
        self.trainer: YOLO = None
        self._yaml_data_dir = yaml_data_dir
        self._pretrained_model_path = pretrained_model_path
        self.is_trained = False

    def train(self, epochs: int, batch_size: int, random_seed: int, output_folder: str, override_data_files: bool):
        """Trains model"""
        if not os.path.exists(self._yaml_data_dir):
            raise ValueError("Directory of yaml file does not exist")
        self.validate_data_dir(self._yaml_data_dir)
        trainer = YOLO(self._pretrained_model_path)
        self.trainer = trainer
        self.trainer.train(data=self._yaml_data_dir, project=output_folder, epochs=epochs, batch=batch_size,
                           seed=random_seed, exist_ok=override_data_files)
        self.is_trained = True

    def evaluate(self, map_metric: MapMetrics):
        """Returns model evaluation metrics for trainer"""
        self._check_trained()

        if map_metric == MapMetrics.MAP50:
            map_score = self.trainer.metrics.box.map50
        elif map_metric == MapMetrics.MAP75:
            map_score = self.trainer.metrics.box.map75
        elif map_metric == MapMetrics.MAP:
            map_score = self.trainer.metrics.box.map
        else:
            raise ValueError("Wrong value for map_metric parameter. Only map50, map75, map values valid.")

        return map_score

    @classmethod
    def validate_data_dir(cls, yaml_data_dir):
        """validate data dir and child folders"""
        if not directory_helper.exists(os.path.join(os.path.dirname(yaml_data_dir), "images")):
            raise ValueError(f"No 'images' directory found in {os.path.dirname(yaml_data_dir)}")
        if not directory_helper.exists(os.path.join(os.path.dirname(yaml_data_dir), "labels")):
            raise ValueError(f"No 'labels' directory found in {os.path.dirname(yaml_data_dir)}")

        original_train_image_dir = cls.get_train_images_dir_path_yaml(yaml_data_dir)
        original_train_labels_dir = cls.get_train_label_dir_path_yaml(yaml_data_dir)
        valid_image_files_dir = cls.get_validation_images_dir_path_yaml(yaml_data_dir)
        valid_labels_dir = cls.get_validation_label_dir_path_yaml(yaml_data_dir)

        cls.validate_image_labels_match(original_train_image_dir, original_train_labels_dir)
        cls.validate_image_labels_match(valid_image_files_dir, valid_labels_dir)

    @classmethod
    def validate_image_labels_match(cls, images_dir: str, labels_dir: str):
        """validation method for images and labels corresponding"""
        all_label_files = [os.path.splitext(ann)[0] for ann in os.listdir(labels_dir)]
        all_img_files = [os.path.splitext(ann)[0] for ann in os.listdir(images_dir)]

        missing_labels = [val for val in all_img_files if val not in all_label_files]
        if missing_labels:
            raise ValueError(
                f"Following images in '{images_dir}' do not have corresponding "
                f"labels: {','.join(missing_labels)}.")

        missing_images = [val for val in all_label_files if val not in all_img_files]
        if missing_images:
            raise ValueError(f"Following labels in '{labels_dir}' "
                             f"do not have corresponding images: {','.join(missing_images)}")

    @classmethod
    def get_validation_images_dir_path_yaml(cls, yaml_file_loc: str):
        """Returns path to validation images folder for given data dir"""
        with open(yaml_file_loc, encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        val_dir = yaml_data.get('val')
        if not directory_helper.exists(val_dir):
            raise ValueError("Images Validation dir does not exists.")
        return val_dir

    @classmethod
    def get_validation_label_dir_path_yaml(cls, yaml_file_loc: str):
        """Returns path to validation images folder for given data dir"""
        with open(yaml_file_loc, encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        val_dir = yaml_data.get('val')
        val_labels_dir = os.path.join(val_dir.replace('images', 'labels'))
        if not directory_helper.exists(val_labels_dir):
            raise ValueError("Labels Validation dir does not exists.")
        return val_labels_dir

    @classmethod
    def get_train_images_dir_path_yaml(cls, yaml_file_loc: str):
        """Returns path to train images folder for given data dir"""
        with open(yaml_file_loc, encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        train_dir = yaml_data.get('train')
        if not directory_helper.exists(train_dir):
            raise ValueError("Images Train dir does not exists.")
        return train_dir

    @classmethod
    def get_train_label_dir_path_yaml(cls, yaml_file_loc: str):
        """Returns path to train images folder for given data dir"""
        with open(yaml_file_loc, encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        train_dir = yaml_data.get('train')
        train_labels_dir = os.path.join(train_dir.replace('images', 'labels'))
        if not directory_helper.exists(train_labels_dir):
            raise ValueError("Labels Train dir does not exists.")
        return train_labels_dir

    @classmethod
    def get_train_images_dir_path(cls, data_dir: str):
        """Returns path to train images folder for given data dir"""
        return os.path.join(data_dir, "images", "train")

    @classmethod
    def get_train_label_dir_path(cls, data_dir: str):
        """Returns path to train annotations folder for given data dir"""
        return os.path.join(data_dir, "labels", "train")

    @classmethod
    def get_validation_images_dir_path(cls, data_dir: str):
        """Returns path to validation images folder for given data dir"""
        return os.path.join(data_dir, "images", "validation")

    @classmethod
    def get_validation_label_dir_path(cls, data_dir: str):
        """Returns path to validation images folder for given data dir"""
        return os.path.join(data_dir, "labels", "validation")

    def _check_trained(self):
        if not self.is_trained:
            raise Exception("Trainer is not trained yet.")
