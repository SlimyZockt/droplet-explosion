from time import time

import cv2
import numpy as np
import logging
import sys
from .Data import SourceData
from .vision import create_mask

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def setup(path: str, settings: list[int]) -> SourceData:
    cap: cv2.VideoCapture = cv2.VideoCapture(path)
    _, firstFrame = cap.read()
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=1,
                                                       varThreshold=100,
                                                       detectShadows=False)
    mask: np.ndarray = create_mask(
        frame=firstFrame, settings=settings,
        background_subtractor=bg_subtractor)
    data: dict[str, list] = {}
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    return SourceData(cap=cap,
                      frame=firstFrame,
                      frame_copy=firstFrame.copy(),
                      mask=mask,
                      data=data,
                      processing_settings=settings,
                      out=cv2.VideoWriter(
                          "./out/mask.avi", fourcc, 20.0, (1280, 720))
                      )


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def process(source_data: SourceData, debug: bool) -> dict[str, list]:

    bg_sub = cv2.createBackgroundSubtractorMOG2(history=1,
                                                varThreshold=100,
                                                detectShadows=False)

    def __init__(self) -> None:
        if not self.cap.isOpened():
            logger.error("Error opening video file")

    def update_data(old_data: dict[str, list], **kwargs) -> dict[str, list]:
        new_data: dict[str, list] = old_data
        for key in kwargs:
            if new_data.get(key) is None:
                new_data[key] = []
            new_data[key].append(kwargs[key])

        return new_data

    def update_frame(video_data: SourceData) -> SourceData:
        new_vd: SourceData = video_data
        new_vd.frame = rescale_frame(new_vd.frame, 50)
        new_vd.frame_copy = new_vd.frame.copy()
        mask = create_mask(
            new_vd.frame, new_vd.processing_settings, background_subtractor=bg_sub)
        # mask = object_detector.apply(new_vd.frame)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        timestamp: float = new_vd.cap.get(
            cv2.CAP_PROP_POS_MSEC)

        new_vd.data = update_data(
            new_vd.data, droplet_count=len(contours),
            time_in_s=timestamp/1000,
            added_size=np.sum(mask == 255))

        cv2.polylines(new_vd.frame, contours, True, (0, 255, 0), 1)

        new_vd.mask = mask

        return new_vd

    def main(source_data: SourceData, debug: bool) -> dict[str, list]:
        count: int = 0
        loop_time: float = time()
        first_frame = source_data.frame_copy

        # Read until video is completed
        while (source_data.cap.isOpened()):

            # Capture frame-by-frame
            ret, source_data.frame = source_data.cap.read()
            source_data.frame = source_data.frame

            if ret:
                # Display the resulting frame
                source_data = update_frame(video_data=source_data)

                out_frame = cv2.cvtColor(source_data.mask, cv2.COLOR_GRAY2BGR)
                source_data.out.write(out_frame)
                if debug:
                    cv2.imshow('frame', source_data.frame)
                    cv2.imshow('mask', source_data.mask)
                    cv2.imshow('original',  source_data.frame_copy)
                logger.debug(f"FPS: {1 / (time() - loop_time)}")
                loop_time = time()

                count += 5
                source_data.cap.set(1, count)

                # pause and play video
                if cv2.waitKey(1) & 0xFF == 32:
                    cv2.waitKey()

                # Press Q on keyboard to  exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        source_data.cap.release()
        source_data.out.release()
        cv2.destroyAllWindows()
        return source_data.data

    return main(source_data, debug)


if __name__ == '__main__':
    import sys
    import re

    path = sys.argv[1]
    temp = re.findall("[\d]", sys.argv[2])
    settings: list[int] = list(map(int, temp))
    source_data: SourceData = setup(path, settings)
    data = process(source_data, True)
