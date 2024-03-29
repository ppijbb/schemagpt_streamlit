import copy
import os
import sys
import cv2
import av
from io import StringIO

from PIL import Image, ImageDraw
import streamlit as st
import streamlit.components.v1 as components

from srcs.st_cache import get_zsc_detector
from srcs.st_style_md import hide_radio_value_md, colorize_multiselect_options


detector = get_zsc_detector()

if 'zsd_labels' not in st.session_state:
    st.session_state.zsd_labels = []
if 'label_colors' not in st.session_state:
    st.session_state.label_colors = ["blue", "green", "orange", "red", "violet", "gray", "rainbow"]


def add_label(label: str):
    st.session_state.zsd_labels.append(f"{label}")


def find_detections(image, labels):
    predictions = detector(image, candidate_labels=labels,)
    draw = ImageDraw.Draw(image)

    for prediction in predictions:
        box = prediction["box"]
        label = prediction["label"]
        score = prediction["score"]
        xmin, ymin, xmax, ymax = box.values()
        draw.rectangle((xmin - 5, ymin - 5, xmax + 5, ymax + 5), outline="red", width=2)
        draw.text((xmin, ymax + 1), f"{label}: {round(score, 2)}", fill="white")

    ImageDraw.Draw(image)
    return image


if __name__ == "__main__":
    st.title('🧫 ZSD Detection & Tracking')
    st.write("this will track the things you want")
    with st.sidebar:
        st.page_link("pages/cardio.py",)
        st.page_link("pages/dep_peptide.py",)
        st.page_link("pages/facial.py",)
        st.page_link("pages/zsd_organoid.py", )

    new_label = st.text_input(
        label="add label",
        placeholder="write label here",
        on_change=colorize_multiselect_options)
    selected_labels = st.multiselect(
        label="the things you want to detect ( max 7 labels )",
        max_selections=7,
        options=st.session_state.zsd_labels,
        default=st.session_state.zsd_labels,
        on_change=colorize_multiselect_options)

    if len(new_label) > 0 and new_label is not None and new_label not in st.session_state.zsd_labels:
        add_label(new_label)
    # colorize_multiselect_options()
    file_video_section, web_video_section, camera_video_section = st.columns(3)
    detect = False
    first_frame = None

    with file_video_section:
        uploaded_file = st.file_uploader("파일 선택", type=["mp4", "mpeg"])
        if uploaded_file is not None:
            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(uploaded_file.__dir__())
            # st.video(uploaded_file)
            uploaded_file.seek(0)
            vod_stream = av.open(uploaded_file, format='mp4').decode(video=0)
            first_frame = next(vod_stream).to_image()

    with web_video_section:
        hide_radio_value_md()
        video_url_selected = st.radio(
            "Select Video in web",
            ["https://github.com/intel-iot-devkit/sample-videos/raw/master/fruit-and-vegetable-detection.mp4",
             "https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4",
             "https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4"],
            captions=["fruit and vegetable.",
                      "bottle",
                      "person bicycle car"])
        if uploaded_file is not None:
            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(uploaded_file.__dir__())
            # st.video(uploaded_file)
            uploaded_file.seek(0)
            vod_stream = av.open(uploaded_file, format='mp4').decode(video=0)
            first_frame = next(vod_stream).to_image()

    with camera_video_section:
        uploaded_file = st.camera_input(label="camera input detection")

        if uploaded_file is not None:
            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(uploaded_file.__dir__())
            # st.video(uploaded_file)
            first_frame = uploaded_file
    if first_frame:
        # image = Image.open('test_img.png')
        with st.spinner('Wait for it...'):
            found_objects = find_detections(image=first_frame, labels=selected_labels)
            st.image(found_objects)
        # cap = cv2.VideoCapture(uploaded_file)
