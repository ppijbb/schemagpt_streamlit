import string
import requests
import cv2
import numpy as np
import av
import json
from typing import List
import os
import inspect

from datetime import datetime as dt
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from streamlit_webrtc.models import VideoProcessorBase
from PIL import ImageFont, ImageDraw, Image
import tensorflow as tf
import keras
from tensorflow.compat.v1 import ConfigProto, InteractiveSession
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image as _IMG

from pages.rtc.public_stun import public_stun_server_list
# from streamlit.components.v1 import html
# import mediapipe as mp

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # 텐서플로가 첫 번째 GPU에 1GB 메모리만 할당하도록 제한
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])
  except RuntimeError as e:
    # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
    print(e)

dir_path = os.getcwd()
# load model
model = model_from_json(open(f"{dir_path}/pages/rtc/caer_face.json", "r").read())
# load weights
model.load_weights(f"{dir_path}/pages/rtc/caer_face.h5")

# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(
#     model_complexity=0,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )

# face detection
cv_path = "/".join(inspect.getfile(cv2).split("/")[:-1])
face_haar_cascade = cv2.CascadeClassifier(f"{cv_path}/data/haarcascade_frontalface_default.xml")
# face_haar_cascade = cv2.CascadeClassifier("C:\\Users\\Lenovo\\.conda\\envs\\python_3_9_env\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")


def process_face(image):
    font_path = f"{dir_path}/font/jalnan/yg-jalnan.ttf"
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

    try:
        image.flags.writeable = False
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
        result = None
        cv2.rectangle(image, (0, 0), (paint_width, 350), (255, 255, 255), thickness=-1)
        cv2.rectangle(image, (0, 0), (start_x + end_x + 60, 80), (196, 196, 196), thickness=-1)
        if 0 < len(faces_detected):
            for (x, y, w, h) in faces_detected:
                # print('WORKING')
                # print(gray_img.shape)

                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), thickness=5) # 얼굴 박스
                roi_gray = gray_img[y - 10:y + w + 10,
                                    x - 10:x + h + 10]  # cropping region of interest i.e. face area from  image
                roi_gray = cv2.resize(roi_gray, (224, 224))
                img_pixels = _IMG.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels *= 0.8

                # print(img_pixels.shape)

                predictions = model.predict(x=img_pixels, verbose=0)
                # find max indexed array

                max_index = np.argmax(predictions[0])

                # emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

                predicted_emotion = emotions[max_index]
                result = {
                    dt.now().strftime("%Y-%m-%dT%H:%M:%S"): {
                          "result": predicted_emotion,
                          "happy": predictions[0][0],
                          "sad": predictions[0][1],
                          "neutral": predictions[0][2]
                    }
                }
                for i, (h, c) in enumerate(zip(labels_y, labels_c)):
                    cv2.line(image, (start_x, h), (int(start_x + end_x * predictions[0][i]), h), c, 13)  # 클래스별 confidence

                image_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(image_pil)
                for n, (index, h) in enumerate(zip(labels, labels_y)):
                    draw.text(xy=(int(3), int(h-5)),
                              text=index,
                              font=font_small,
                              fill=(0, 0, 0, 0))
                    draw.text(xy=(int(end_x+50), int(h-5)),
                              text=str(np.round(predictions[0][n], 3)),
                              font=font_small,
                              fill=(0, 0, 0, 0))
                draw.text(xy=(int(paint_width / 1.55), int(20)),
                          text=labels[max_index],
                          font=font_regular,
                          fill=(0, 0, 0, 0))
                # draw.text(xy=(int(x+10), int(y-30)), # 얼굴 박스에 라벨 보여주기
                #           text=labels[max_index],
                #           font=font_regular,
                #           fill=(255, 0, 0, 0))
                processed = np.array(image_pil)
        else:
            for h, c in zip(labels_y, labels_c):
                cv2.line(image, (start_x, h), (int(start_x + end_x * 0.0005), h), c, 10)  # 클래스별 confidence

            image_pil = Image.fromarray(image)
            draw = ImageDraw.Draw(image_pil)
            for l, h in zip(labels, labels_y):
                draw.text(xy=(int(3), int(h-5)),
                          text=l,
                          font=font_small,
                          fill=(0, 0, 0, 0))
                draw.text(xy=(int(end_x+50), int(h-5)),
                          text="0.00",
                          font=font_small,
                          fill=(0, 0, 0, 0))
            draw.text(xy=(int(paint_width / 2), int(20)),
                      text="얼굴이 인식되지 않았습니다.",
                      font=font_regular_small,
                      fill=(0, 0, 0, 0))
            processed = np.array(image_pil)
        return processed, result

    except Exception as e:
        print("Exception", e)
        for h, c in zip(labels_y, labels_c):
            cv2.line(image, (start_x, h), (int(start_x + end_x * 0.0005), h), c, 10)  # 클래스별 confidence
        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)
        for index, h in zip(labels, labels_y):
            draw.text(xy=(int(3), int(h-5)),
                      text=index,
                      font=font_small,
                      fill=(0, 0, 0, 0))
            draw.text(xy=(int(end_x + 50), int(h - 5)),
                      text="0.00",
                      font=font_small,
                      fill=(0, 0, 0, 0))
        draw.text(xy=(int(paint_width / 2), int(20)),
                  text="얼굴이 인식되지 않았습니다.",
                  font=font_regular_small,
                  fill=(0, 0, 0, 0))
        processed = np.array(image_pil)
        return processed, None


# def process(image):
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image)
#
#     # Draw the hand annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#       for hand_landmarks in results.multi_hand_landmarks:
#         mp_drawing.draw_landmarks(
#             image,
#             hand_landmarks,
#             mp_hands.HAND_CONNECTIONS,
#             mp_drawing_styles.get_default_hand_landmarks_style(),
#             mp_drawing_styles.get_default_hand_connections_style())
#     return image
#     # return cv2.flip(image, 1)


RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": public_stun_server_list
            },
            # {
            #     "urls": "turn:openrelay.metered.ca:80",
            #     "username": "openrelayproject",
            #     "credential": "openrelayproject",
            # },
            # {
            #     "urls": "turn:openrelay.metered.ca:443",
            #     "username": "openrelayproject",
            #     "credential": "openrelayproject",
            # },
            # {
            #     "urls": "turn:openrelay.metered.ca:443?transport=tcp",
            #     "username": "openrelayproject",
            #     "credential": "openrelayproject",
            # },
            # {
            #     "urls": "turn:numb.viagenie.ca",
            #     "username": 'webrtc@live.com',
            #     "credential": 'muazkh'
            # },
            # {
            #     "urls": "turn:192.158.29.39:3478?transport=udp",
            #     "username": '28224511:1379330808',
            #     "credential": 'JZEOEt2V3Qb0y27GRntt2u2PAYA='
            # },
            # {
            #     "urls": "turn:192.158.29.39:3478?transport=tcp",
            #     "username": '28224511:1379330808',
            #     "credential": 'JZEOEt2V3Qb0y27GRntt2u2PAYA='
            # }
        ]
    }
)


class VideoProcessor(VideoProcessorBase):
    result_dict = dict()
    code = None

    def recv(self, frame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        img, _result = process_face(img)
        # img = process(img)
        # if _result:
        #     self.result_dict.update(_result)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    async def recv_queued(self, frames: List[av.VideoFrame]) -> List[av.VideoFrame]:
        return [self.recv(frames[-1])]

    def on_ended(self):
        print("############### Connection Ended #################")
        # data = f"{self.result_dict}".replace("\'", "\"")
        data = None

        if data:
            requests.post(
                f"http://localhost:5000/caer/face?state=start&name={self.code}",
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=utf-8'
                },
                json=json.loads(data)
            )
        else:
            print("error")

# @st.cache(suppress_st_warning=True)
def show():
    # queries = st.experimental_get_query_params()
    # code = queries.get("code", None)[0]
    webrtc_ctx = webrtc_streamer(
        key=string.punctuation,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={
            "video": {
                "frameRate": {
                    "max": 30,
                    "ideal": 1
                },
                "width": {
                    "min": 640,
                    "max": 1024
                },
                "height": {
                    "min": 480,
                    "max": 768
                },
            },
            "audio": True
        },
        video_processor_factory=VideoProcessor,
        async_processing=True,
        desired_playing_state=True,
        video_html_attrs={
            "style": {
                "width": "100%",
                "max-width": "768px",
                "margin": "0 auto",
                "justify-content": "center"
            },
            "controls": True,
            "autoPlay": False
        },
    )
    if webrtc_ctx.state.signalling:
        webrtc_ctx.video_processor.code = None


if __name__ == "__main__":
    st.set_page_config(
        page_title="CAERScope",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title('🦜🔗 Quickstart App')
    with st.sidebar:
        st.page_link("pages/cardio.py",)
        st.page_link("pages/dep_peptide.py",)
        st.page_link("pages/facial.py",)
    # hide_menu_style = """
    #         <style>
    #         .css-1avcm0n {visibility: hidden;}
    #         .css-18ni7ap {visibility: hidden;}
    #         .block-container {padding: 0rem 1rem 10rem;}
    #         .block-container div {justify-content: center;gap: 0rem;}
    #         video {}
    #         </style>
    #         """
    # st.markdown(hide_menu_style, unsafe_allow_html=True)
    show()
