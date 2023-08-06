"""Includes ObjectDetector class"""
import os
from typing import List, Dict

from ultralytics import YOLO

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.object_detection.services.object_detection_trainer import ObjectDetectionTrainer
from organon.ml.object_detection.services.objects.detection_info import DetectionInfo


class ObjectDetector:
    """Class for detecting objects in images using a trained model"""

    def __init__(self, pretrained_model_path: str):
        """
        Initializes ObjectDetector to use a pretrained model for detection

        """
        self.model_path = None
        self._detector = None
        self.pretrained_model_path = None

        if pretrained_model_path != -1:
            self._validate_pretrained_model_path(pretrained_model_path)
            self.pretrained_model_path = pretrained_model_path

            try:
                self._detector = YOLO(pretrained_model_path)
            except Exception as exc:
                msg = "Error occurred while loading pretrained model. " \
                      "Make sure the model in given path is a pretrained model." \
                      "If you want to run detection with a model you trained using ObjectDetectionTrainer," \
                      "use from_custom_model classmethod to initialize the detector."
                LogHelper.error(msg)
                raise Exception(msg) from exc

    def detect(self, input_image_path: str, output_folder: str = None, objects_to_detect: List[str] = None,
               save: bool = True, save_txt: bool = True) -> List[DetectionInfo]:
        """
        Detect object in input image.
        :param input_image_path: Path to image to detect objects from
        :param objects_to_detect: List of objects to detect in image. Cannot be used for detection with custom models.
            To see all available objects for detection call 'get_all_object_names' method.
        """
        if output_folder is not None:
            if not os.path.exists(output_folder):
                raise ValueError("Output Folder path does not exists.")

        results = self._get_detections(input_image_path, objects_to_detect=objects_to_detect, save=save,
                                       save_txt=save_txt, output_folder=output_folder)
        detection_info = []
        if results:
            for detection in results:
                detection_info.append(DetectionInfo(object_name=detection.boxes.cls, confidence=detection.boxes.conf,
                                                    box_points=detection.boxes.xyxy))
        return detection_info

    def _get_detections(self, input_image_path: str, output_folder: str = None,
                        objects_to_detect: List[str] = None, save: bool = True,
                        save_txt: bool = True):

        if self.model_path:
            if objects_to_detect:
                raise NotImplementedError("objects_to_detect feature is not implemented for detection with "
                                          "custom trained models")
        try:
            if objects_to_detect:
                object_key_list = self._validate_objects_to_detect(objects_to_detect)

                if output_folder is not None:
                    results = self._detector(input_image_path,
                                             save=save, save_txt=save_txt, classes=object_key_list,
                                             project=output_folder)
                else:
                    results = self._detector(input_image_path,
                                             save=save, save_txt=save_txt, classes=object_key_list,
                                             project=os.path.dirname(input_image_path))
            else:
                if output_folder is not None:
                    results = self._detector(input_image_path, save=save, save_txt=save_txt, project=output_folder)
                else:
                    results = self._detector(input_image_path, save=save, save_txt=save_txt,
                                             project=os.path.dirname(input_image_path))
        except Exception as exc:
            raise exc

        return results

    def get_all_object_names(self) -> Dict:
        """Returns all object available for detection"""
        return self._detector.names

    @classmethod
    def from_custom_model(cls, model_path: str):
        """
        Initializes ObjectDetector to use a custom trained model for detection

        :param str model_path: Path of a model trained with ObjectDetectionTrainer. Should be given if you will not use
            the pretrained model.
        """
        detector = ObjectDetector(pretrained_model_path=-1)
        detector.model_path = model_path
        detector._detector = YOLO(model_path)
        return detector

    @classmethod
    def load_pretrained_model_from_web(cls, target_path: str,
                                       model_type: str = "small"):
        """Loads a pretrained model to given file path after downloading from web. The default model to be downloaded is
        'YOLOv8s' and its approx 25 MB
        :param target_path: File path to download the pretrained model in
        :param model_type: Model type keyword to be downloaded
        """
        ObjectDetectionTrainer.load_pretrained_model_from_web(target_path, model_type=model_type)

    @classmethod
    def _validate_pretrained_model_path(cls, pretrained_model_path: str):
        if pretrained_model_path is None:
            raise ValueError("Please enter pretrained_model_path. You can use 'load_pretrained_model_from_web'"
                             " method to load a model from internet to a file.")
        if not os.path.isfile(pretrained_model_path):
            raise ValueError(f"No model file found in {pretrained_model_path}.")

    def _validate_objects_to_detect(self, object_names: List[str]):
        all_obj_names = self.get_all_object_names()
        non_existing_objects = [val for val in object_names if val not in all_obj_names.values()]
        if non_existing_objects:
            raise ValueError(f"Following objects cannot be detected by model: {','.join(non_existing_objects)}."
                             " Call get_all_object_names to see valid object names")
        object_key_list = [key for key, value in all_obj_names.items() if value in object_names]

        return object_key_list
