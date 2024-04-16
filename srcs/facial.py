import requests
import cv2
import numpy as np
import av
import json
from typing import List
import os
from datetime import datetime as dt

from PIL import ImageFont, ImageDraw, Image
import speech_recognition as sr
import tensorflow as tf
import keras
from tensorflow.compat.v1 import ConfigProto, InteractiveSession
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image as _IMG
from streamlit_webrtc.models import VideoProcessorBase, AudioProcessorBase
import speech_recognition as sr
from srcs.st_cache import get_facial_processors

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # 텐서플로가 첫 번째 GPU에 1GB 메모리만 할당하도록 제한
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=768)])
  except RuntimeError as e:
    # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
    print(e)


dir_path = os.getcwd()
model, face_haar_cascade = get_facial_processors(path=dir_path)


def process_face(image):
    font_path = f"{dir_path}/pages/font/jalnan/yg-jalnan.ttf"
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
        image.flags.writeable = True
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
        result = None
        cv2.rectangle(image, (0, 0), (paint_width, 80), (255, 255, 255), -1)
        cv2.rectangle(image, (0, 0), (start_x + end_x + 60, 80), (196, 196, 196), -1)
        if 0 < len(faces_detected):
            for (x, y, w, h) in faces_detected:
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), thickness=5) # 얼굴 박스
                roi_gray = gray_img[y - 10:y + w + 10,
                                    x - 10:x + h + 10]  # cropping region of interest i.e. face area from  image
                roi_gray = cv2.resize(roi_gray, (224, 224))
                img_pixels = _IMG.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels *= 0.8
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
        result = None

    return processed, result


class AudioProcessor(AudioProcessorBase):
    result_dict = dict()
    code = None
    recognizer = sr.Recognizer()

    def array_to_audiodata(self, audio_array, sample_rate):
        # print(audio_array.shape)
        return sr.AudioData(frame_data=audio_array.tobytes(),
                            sample_rate=sample_rate,
                            sample_width=2)

    def recv(self, frame) -> av.AudioFrame:
        try:
            audio_data = self.array_to_audiodata(audio_array=frame.to_ndarray(),
                                                 sample_rate=frame.sample_rate)
            print(self.recognizer.recognize_google(audio_data, language="ko", show_all=True))
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("요청 에러:", e)
        return frame

    async def recv_queued(self, frames: List[av.AudioFrame]) -> List[av.AudioFrame]:
        return [self.recv(frames[-1])]

    def on_ended(self):
        print("############### Connection Ended #################")


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
            print("Not send results")
