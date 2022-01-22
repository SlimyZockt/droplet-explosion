from dataclasses import dataclass
from enum import Enum
import cv2
import numpy as np


@dataclass(order=True)
class SourceData():
    cap: cv2.VideoCapture
    frame: np.ndarray
    frame_copy: np.ndarray
    mask: np.ndarray
    data: dict[str, list]
    processing_settings: list[int]
    out: cv2.VideoWriter


class ProcessingSettings(Enum):
    COLOR_FILTERING = 0
    EDGE_DETECTION = 1
    SUBTRACTOR_MOG2 = 2
