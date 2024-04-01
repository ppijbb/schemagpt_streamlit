import av
import string
import asyncio
from io import BytesIO

from PIL import Image, ImageDraw
import streamlit as st

from streamlit_webrtc import webrtc_streamer, WebRtcMode

from pages.rtc.config import RTC_CONFIGURATION
from srcs.object_tracking import VideoProcessor, find_detections, img_convert
from srcs.object_tracking import ArrayMediaPlayer, get_media_player
from srcs.st_style_md import hide_radio_value_md, colorize_multiselect_options


colorize_multiselect_options()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

if 'zsd_labels' not in st.session_state:
    st.session_state.zsd_labels = ["bottle", "car", "bicycle", "a handsome guy", "green fruit"]
if 'target_image' not in st.session_state:
    st.session_state.target_image = Image.new("RGB", (800, 1280), (255, 255, 255))
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'normalizing_range' not in st.session_state:
    st.session_state.normalizing_range = [0, 198]
if 'bright_ratio' not in st.session_state:
    st.session_state.bright_ratio = 1.0
if 'use_normalizing' not in st.session_state:
    st.session_state.use_normalizing = False
if 'use_denosing_color' not in st.session_state:
    st.session_state.use_denosing_color = False
if 'use_morphology' not in st.session_state:
    st.session_state.use_morphology = False
if 'detected_objects' not in st.session_state:
    st.session_state.detected_objects = []
if not any([k for k in st.session_state if 'denoising_color' in k]):
    st.session_state.denoising_color0 = 10
    st.session_state.denoising_color1 = 10
    st.session_state.denoising_color2 = 7
    st.session_state.denoising_color3 = 21
if not any([k for k in st.session_state if 'morphology_kernel' in k]):
    st.session_state.morphology_kernel0 = 18
    st.session_state.morphology_kernel1 = 18
if 'detect_button' not in st.session_state:
    st.session_state.detect_button = False
if 'image_source' not in st.session_state:
    st.session_state.image_source = "web"  # web/file/cam
if 'start_rtc_detecting' not in st.session_state:
    st.session_state.start_rtc_detecting = False


def add_label(label: str):
    st.session_state.zsd_labels.append(f"{label}")


def detect_button_click():
    st.session_state.detect_button = True


def onchange_radio():
    if bool(st.session_state.camera_image):
        st.session_state.camera_image.close()
    st.session_state.camera_image = None
    if bool(st.session_state.uploaded_file):
        st.session_state.uploaded_file.close()
    st.session_state.uploaded_file = None
    colorize_multiselect_options()


def onchange_file():
    if bool(st.session_state.camera_image):
        st.session_state.camera_image.close()
    st.session_state.camera_image = None
    st.session_state.video_url_selected = None
    colorize_multiselect_options()


def onchange_webcam():
    if bool(st.session_state.uploaded_file):
        st.session_state.uploaded_file.close()
    st.session_state.uploaded_file = None
    st.session_state.video_url_selected = None
    colorize_multiselect_options()


if __name__ == "__main__":
    st.title('🧫 ZSD Detection & Tracking')
    st.write("this will track the things you want")

    # with st.sidebar:
    #     st.page_link("pages/cardio.py",)
    #     st.page_link("pages/dep_peptide.py",)
    #     st.page_link("pages/facial.py",)
    #     st.page_link("pages/zsd_organoid.py", )

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
    st.divider()
    file_video_section, web_video_section, camera_video_section = st.columns(3)
    detect = False
    st.session_state.original_image = None
    vod_stream = None
    found_objects = None

    # uploaded file processing
    with file_video_section:
        st.session_state.uploaded_file = st.file_uploader("파일 선택",
                                                          type=["mp4", "mpeg"],
                                                          on_change=onchange_file)
        if st.session_state.uploaded_file is not None:
            st.session_state.uploaded_file.seek(0)
            vod_stream = av.open(st.session_state.uploaded_file, format='mp4')
            vod_generator = vod_stream.decode(video=0)
            st.session_state.original_image = next(vod_generator).to_image()
            st.session_state.target_image = st.session_state.original_image
            st.session_state.image_source = "file"

    # web video file processing
    with web_video_section:
        hide_radio_value_md()
        st.radio(
            label="Select Video in web",
            options=["https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4",
                     "https://github.com/intel-iot-devkit/sample-videos/raw/master/fruit-and-vegetable-detection.mp4",
                     "https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4"],
            captions=["bottle",
                      "fruit and vegetable.",
                      "person bicycle car"],
            key="video_url_selected",
            on_change=onchange_radio)
        if st.session_state.video_url_selected is not None:
            vod_stream = av.open(st.session_state.video_url_selected, format='mp4')
            vod_generator = vod_stream.decode(video=0)
            st.session_state.original_image = next(vod_generator).to_image()
            st.session_state.target_image = st.session_state.original_image
            st.session_state.image_source = "web"

    # webcam(if) video processing
    with camera_video_section:
        st.session_state.camera_image = st.camera_input(label="camera input detection",
                                                        on_change=onchange_webcam)
        if st.session_state.camera_image is not None:
            vod_stream = None
            # st.session_state.original_image = camera_image.getvalue()
            st.session_state.original_image = Image.open(st.session_state.camera_image)
            st.session_state.target_image = st.session_state.original_image
            st.session_state.image_source = "cam"

    st.divider()
    control_section, detection_section = st.columns((0.3, 0.7))
    with control_section:
        st.slider(label="bright",
                  min_value=0.0,
                  max_value=10.0,
                  step=0.01,
                  key="bright_ratio",
                  on_change=colorize_multiselect_options)
        st.toggle(label="normalizing",
                  key="use_normalizing")
        st.slider(label="normalize",
                  min_value=0,
                  max_value=255,
                  key="normalizing_range",
                  on_change=colorize_multiselect_options,
                  label_visibility="collapsed")
        st.toggle(label="denoising color",
                  key="use_denoising_color")
        for i, c in enumerate(st.columns(4)):
            c.number_input(label=f"denoising color",
                           key=f"denoising_color{i}",
                           step=1,
                           on_change=colorize_multiselect_options,
                           label_visibility="collapsed")
        st.toggle(label="morphology color",
                  key="use_morphology")
        for i, c in enumerate(st.columns(2)):
            c.number_input(label=f"morphology kernel",
                           key=f"morphology_kernel{i}",
                           step=1,
                           on_change=colorize_multiselect_options,
                           label_visibility="collapsed")
        st.button(label="detect!",
                  on_click=detect_button_click)
    with detection_section:
        with st.container(border=True,):
            if bool(st.session_state.original_image):
                st.session_state.target_image = img_convert(st.session_state.original_image)
                st.image(image=st.session_state.target_image,
                         use_column_width="always")
                if st.session_state.detect_button:
                    with st.spinner('Detecting objects... it takes time....'):
                        found_objects = find_detections(image=st.session_state.target_image,
                                                        labels=selected_labels,)
                # cap = cv2.VideoCapture(uploaded_file)
                    st.image(image=found_objects["image"],
                             use_column_width="always")
                    st.session_state.detect_button = False
                    st.session_state.detected_objects = found_objects["predictions"]

    st.divider()
    with st.spinner("Real-time tracking is currently being prepared..."):
        if st.session_state.detected_objects:
            if st.session_state.image_source == "cam":
                player_factory = ArrayMediaPlayer(vod_stream) if found_objects and vod_stream is not None else None
                webrtc_ctx = webrtc_streamer(
                    key=string.punctuation,
                    mode=WebRtcMode.SENDRECV,
                    rtc_configuration=RTC_CONFIGURATION,
                    media_stream_constraints={
                        "video": {
                            "frameRate": {
                                "max": 60,
                                "ideal": 30
                            },
                            "width": {
                                "min": 320,
                                "max": 1024
                            },
                            "height": {
                                "min": 240,
                                "max": 768
                            },
                        },
                        "audio": True
                    },
                    # video_processor_factory=VideoProcessor,
                    player_factory=get_media_player("https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4",),
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
            elif st.session_state.image_source == "web":
                player_factory = (lambda x: ArrayMediaPlayer(vod_stream)) if found_objects and vod_stream is not None else None
                webrtc_ctx = webrtc_streamer(
                    key=string.punctuation,
                    mode=WebRtcMode.SENDRECV,
                    rtc_configuration=RTC_CONFIGURATION,
                    media_stream_constraints={
                        "video": {
                            # "frameRate": {
                            #     "max": 60,
                            #     "ideal": 1
                            # },
                            "width": {
                                "min": 320,
                                "max": 1024
                            },
                            "height": {
                                "min": 240,
                                "max": 768
                            },
                        },
                        "audio": True
                    },
                    # video_processor_factory=player_factory,
                    player_factory=player_factory,
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
            else:
                st.write("real time detecting activate after capture")
