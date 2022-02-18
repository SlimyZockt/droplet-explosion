import numpy as np
import cv2


def create_black_img(height: int, width: int):
    return np.zeros((height, width, 1), dtype="uint8")


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
