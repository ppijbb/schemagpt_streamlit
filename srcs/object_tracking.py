from typing import List
import os
from typing import Optional, Set
import threading

import cv2
import numpy as np
import av
from PIL import ImageFont, ImageDraw, Image
from aiortc.contrib.media import MediaPlayer, PlayerStreamTrack, REAL_TIME_FORMATS

import streamlit as st
from streamlit_webrtc.models import VideoProcessorBase

from srcs.st_cache import get_zsc_detector

detector = get_zsc_detector()


class ArrayMediaPlayer(MediaPlayer):
    def __init__(
        self, file, format=None, options=None, timeout=None, loop=False, decode=True
    ):
        self.__container = file
        self.__thread: Optional[threading.Thread] = None
        self.__thread_quit: Optional[threading.Event] = None

        # examine streams
        self.__started: Set[PlayerStreamTrack] = set()
        self.__streams = []
        self.__decode = decode
        self.__audio: Optional[PlayerStreamTrack] = None
        self.__video: Optional[PlayerStreamTrack] = None
        for stream in self.__container.streams:
            if stream.type == "audio" and not self.__audio:
                if self.__decode:
                    self.__audio = PlayerStreamTrack(self, kind="audio")
                    self.__streams.append(stream)
                elif stream.codec_context.name in ["opus", "pcm_alaw", "pcm_mulaw"]:
                    self.__audio = PlayerStreamTrack(self, kind="audio")
                    self.__streams.append(stream)
            elif stream.type == "video" and not self.__video:
                if self.__decode:
                    self.__video = PlayerStreamTrack(self, kind="video")
                    self.__streams.append(stream)
                elif stream.codec_context.name in ["h264", "vp8"]:
                    self.__video = PlayerStreamTrack(self, kind="video")
                    self.__streams.append(stream)

        # check whether we need to throttle playback
        container_format = set(self.__container.format.name.split(","))
        self._throttle_playback = not container_format.intersection(REAL_TIME_FORMATS)

        # check whether the looping is supported
        assert (
            not loop or self.__container.duration is not None
        ), "The `loop` argument requires a seekable file"
        self._loop_playback = loop


class VideoProcessor(VideoProcessorBase):
    result_dict = dict()
    code = None
    dir_path = os.getcwd()

    def recv(self, frame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        img, _result = self.process_video(img)
        # img = process(img)
        # if _result:
        #     self.result_dict.update(_result)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    async def recv_queued(self, frames: List[av.VideoFrame]) -> List[av.VideoFrame]:
        return [self.recv(frames[-1])]

    def on_ended(self):
        """
        TODO : add what will do something in the end
        """
        print("############### Connection Ended #################")

    def process_video(self, image):
        font_path = f"{self.dir_path}/pages/font/jalnan/yg-jalnan.ttf"
        font_regular = ImageFont.truetype(font=font_path, size=35)
        font_regular_small = ImageFont.truetype(font=font_path, size=18)
        font_small = ImageFont.truetype(font=font_path, size=16)
        paint_width = image.shape[1]
        emotions = ['happy', 'sad', 'neutral']
        labels = ["긍정", "부정", "중립"]
        labels_y = [10, 40, 65]
        labels_c = [(0, 255, 0), (0, 0, 255), (125, 125, 125)]
        start_x = int(40)
        end_x = int(paint_width / 4)

        return image


def img_convert(img) -> np.array:
    if isinstance(img, Image.Image):
        img = np.array(img)
    if st.session_state.use_normalizing:
        img = cv2.normalize(img, None,
                            st.session_state.normalizing_range[0],
                            st.session_state.normalizing_range[1],
                            cv2.NORM_MINMAX)  # Normalizing frame
    if st.session_state.use_denosing_color:
        img = cv2.fastNlMeansDenoisingColored(img, None,
                                              st.session_state.denoising_color0,
                                              st.session_state.denoising_color1,
                                              st.session_state.denoising_color2,
                                              st.session_state.denoising_color3)
    if st.session_state.use_morphology:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                           (st.session_state.morphology_kernel0,
                                            st.session_state.morphology_kernel1),)
        # tophat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, kernel) # Apply top hat operation
        tophat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, kernel)  # Apply top hat operation
        img = np.stack([tophat, tophat, tophat], axis=2)
    img = (img * st.session_state.bright_ratio).astype(np.uint8)
    return img


def find_detections(image, labels, st_state):
    image = Image.fromarray(image)
    predictions = detector(image,
                           candidate_labels=labels,)
    draw = ImageDraw.Draw(image)
    st_state = predictions
    for prediction in predictions:
        box = prediction["box"]
        label = prediction["label"]
        score = prediction["score"]
        xmin, ymin, xmax, ymax = box.values()
        draw.rectangle((xmin - 5, ymin - 5, xmax + 5, ymax + 5), outline="red", width=2)
        draw.text((xmin, ymax + 1), f"{label}: {round(score, 2)}", fill="white")

    ImageDraw.Draw(image)
    return image


def track(st_state):
    w_l = []
    h_l = []
    windows = []
    roi_hists = []

    for prediction in st_state:
        box = prediction['box']
        data = [
            box['xmin'] - 7, box['ymin'] - 7,
            box['xmax'] + 7, box['ymax'] + 7,
        ]
        w_l += [box["xmax"] - box["xmin"]]
        h_l += [box["ymax"] - box["ymin"]]
        windows += [data]

        roi = st.session_state.target_image[box["ymin"]:box["ymax"], box["xmin"]:box["xmax"]]
        hsv_roi = cv2.cvtColor(st.session_state.target_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        roi_hists += [roi_hist]
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    return None
