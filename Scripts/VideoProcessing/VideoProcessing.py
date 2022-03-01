import cv2
import numpy as np
import logging
from .vision import create_mask
from time import time


def generate_data_from_src(path: str, debug: bool, frame_skip_rate: int = 5):
    cap: cv2.VideoCapture = cv2.VideoCapture(path)
    count: int = 0
    data: dict[str, list] = {}

    loop_time: float = time()

    # width = cap.get(3)
    # height = cap.get(4)

    bg_sub = cv2.createBackgroundSubtractorMOG2(history=1,
                                                varThreshold=100,
                                                detectShadows=False)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # init
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    # init
    if not cap.isOpened():
        logger.error("Error opening video file")

    def update_data(old_data: dict[str, list], **kwargs) -> dict[str, list]:
        new_data: dict[str, list] = old_data
        for key in kwargs:
            if new_data.get(key) is None:
                new_data[key] = []
            new_data[key].append(kwargs[key])

        return new_data

    # TODO: process frame and create mask

    def process_frame(frame: np.ndarray):
        mask = create_mask(frame, background_subtractor=bg_sub)

        contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        timestamp: float = cap.get(cv2.CAP_PROP_POS_MSEC)

        if debug:
            cv2.imshow('original_frame', frame)
            cv2.imshow('mask', mask)

        return {
            'droplet_count': len(contours),
            'time_in_s': timestamp/1000,
            'added_size': np.sum(mask == 255)
        }

    frame_win = cv2.namedWindow('original_frame', cv2.WINDOW_GUI_EXPANDED)
    mask_win = cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    
    while (cap.isOpened()):
        ret, og_frame = cap.read()

        if ret:
            frame_data = process_frame(og_frame)
            data = update_data(data, **frame_data)

            logger.debug(f"FPS: {1 / (time() - loop_time)}")
            loop_time = time()

            count += frame_skip_rate

            cap.set(1, count)

            # Press Space to pause/play video
            if cv2.waitKey(1) & 0xFF == 32:
                cv2.waitKey()

            # Press Q on keyboard to  exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return data
