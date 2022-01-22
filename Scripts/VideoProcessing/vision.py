import cv2
import numpy as np


def _mask_form_color(frame: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([1, 35, 40])
    upper_blue = np.array([230, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    return mask


def create_mask(frame: np.ndarray, settings: list[int], background_subtractor) -> np.ndarray:
    # creates black img with the shape of frame
    shape = (frame.shape[0], frame.shape[1], 1)
    black_img = np.zeros(shape, dtype="uint8")
    # uses Canny Edge Detection to create a mask
    # removed_bg = background_subtractor.apply(frame) if (3 in settings) else black_img
    edge_mask = cv2.Canny(frame, 42, 146) if (1 in settings) else black_img
    color_mask = _mask_form_color(frame) if (0 in settings) else black_img

    mask = cv2.add(edge_mask, color_mask)
    # mask = cv2.add(mask, removed_bg)

    return mask
