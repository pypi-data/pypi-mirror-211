"""Includes DetectionInfo class."""
from typing import List


class DetectionInfo:
    """Information generated for a detected object in an image"""

    def __init__(self, object_name: str, confidence: float, box_points: List[int]):
        self.object_name = object_name
        self.confidence = confidence
        self.box_points = box_points
