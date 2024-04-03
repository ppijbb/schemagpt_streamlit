import av
import string
import asyncio
from io import BytesIO

from PIL import Image, ImageDraw
import streamlit as st

from streamlit_webrtc import webrtc_streamer, WebRtcMode

from pages.rtc.config import RTC_CONFIGURATION
from pages.rtc.public_stun import public_stun_server_list
from srcs.object_tracking import VideoProcessor, detect_objects_in_image, img_convert
from srcs.object_tracking import MediaPlayer, get_media_player
from srcs.st_style_md import hide_radio_value_md, colorize_multiselect_options


colorize_multiselect_options()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

if 'zsd_labels' not in st.session_state:
    st.session_state.zsd_labels = ["a water bottle", "car", "bicycle", "a handsome guy", "green fruit"]
if 'target_image' not in st.session_state:
    st.session_state.target_image = Image.new("RGB", (800, 1280), (255, 255, 255))
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'detected_image' not in st.session_state:
    st.session_state.detected_image = None
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
if 'vod_stream' not in st.session_state:
    st.session_state.vod_stream = None
if 'detect_button' not in st.session_state:
    st.session_state.detect_button = False
if 'image_source' not in st.session_state:
    st.session_state.image_source = "web"  # web/file/cam
if 'video_url_selected' not in st.session_state:
    st.session_state.video_url_selected = "https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4"
if 'start_rtc_detecting' not in st.session_state:
    st.session_state.start_rtc_detecting = False


def add_label(label: str):
    st.session_state.zsd_labels.append(f"{label}")


def detect_button_click():
    st.session_state.detect_button = True


def onchange_image():
    if st.session_state.original_image is not None:
        del st.session_state["original_image"]
    st.session_state.original_image = None
    colorize_multiselect_options()


def onchange_web():
    st.session_state.image_source = "web"
    onchange_image()


def onchange_file():
    st.session_state.image_source = "file"
    onchange_image()


def onchange_cam():
    st.session_state.image_source = "cam"
    onchange_image()


def get_web_media():
    url = "https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4"
    return get_media_player(url=url)


if __name__ == "__main__":
    st.title('🧫 ZSD Detection & Tracking')
    st.write("입력받은 라벨을 찾아드립니다.")

    # with st.sidebar:
    #     st.page_link("pages/cardio.py",)
    #     st.page_link("pages/dep_peptide.py",)
    #     st.page_link("pages/facial.py",)
    #     st.page_link("pages/zsd_organoid.py", )

    new_label = st.text_input(
        label="라벨 추가하기",
        placeholder="write label here with english",
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
    # st.session_state.original_image = None
    st.session_state.vod_stream = None
    found_objects = None

    # uploaded file processing
    with file_video_section:
        st.file_uploader("파일 선택",
                         type=["mp4", "mpeg"],
                         key="uploaded_file",
                         on_change=onchange_file)
        if st.session_state.uploaded_file is not None and st.session_state.image_source == "file":
            st.session_state.uploaded_file.seek(0)
            st.session_state.vod_stream = av.open(st.session_state.uploaded_file, format='mp4')
            vod_generator = st.session_state.vod_stream.decode(video=0)
            st.session_state["original_image"] = next(vod_generator).to_image()
            st.session_state.target_image = st.session_state.original_image

    # web video file processing
    with web_video_section:
        hide_radio_value_md()
        st.radio(
            label="Select Video in web",
            options=["https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4",
                     "https://github.com/intel-iot-devkit/sample-videos/raw/master/fruit-and-vegetable-detection.mp4",
                     "https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4",],
            captions=["물병",
                      "과일과 야채",
                      "사람 자전거 차량",],
            key="video_url_selected",
            on_change=onchange_web)
        if st.session_state.video_url_selected is not None and st.session_state.image_source == "web":
            st.session_state.vod_stream = av.open(st.session_state.video_url_selected, format='mp4')
            vod_generator = st.session_state.vod_stream.decode(video=0)
            st.session_state.original_image = None
            st.session_state["original_image"] = next(vod_generator).to_image()
            st.session_state.target_image = st.session_state.original_image

    # webcam(if) video processing
    with camera_video_section:
        st.camera_input(label="camera input detection",
                        on_change=onchange_cam,
                        key="camera_image")
        # print("camera", st.session_state.camera_image)
        if st.session_state.camera_image is not None and st.session_state.image_source == "cam":
            st.session_state.vod_stream = None
            # st.session_state.original_image = camera_image.getvalue()
            st.session_state["original_image"] = Image.open(st.session_state.camera_image)
            st.session_state.target_image = st.session_state.original_image

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
            if st.session_state.original_image is not None:
                st.session_state.target_image = img_convert(st.session_state.original_image)
                st.image(image=st.session_state.target_image,
                         use_column_width="always")
                if st.session_state.detect_button:
                    with st.spinner('Detecting objects... it takes time....'):
                        found_objects = detect_objects_in_image(image=st.session_state.target_image,
                                                                labels=selected_labels, )
                        st.session_state.detected_objects = found_objects["predictions"]
                        if bool(found_objects):
                            st.session_state.detected_image = found_objects["image"]
                        else:
                            st.session_state.detected_image = st.session_state.target_image
                    st.session_state.detect_button = False

                if st.session_state.detected_image is not None:
                    st.image(image=st.session_state.detected_image,
                             use_column_width="always")

    st.divider()
    if st.session_state.detected_objects:
        with st.spinner("Real-time tracking is currently being prepared..."):
            video_factory = VideoProcessor(predictions=st.session_state.detected_objects,
                                           image=st.session_state.target_image)
            vod_stream = st.session_state.vod_stream
            webrtc_ctx = webrtc_streamer(
                key=string.punctuation,
                mode=WebRtcMode.RECVONLY if st.session_state.image_source == "web" else WebRtcMode.SENDRECV,
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
                video_processor_factory=video_factory,
                player_factory=(lambda x=0: MediaPlayer(file=vod_stream)) if st.session_state.image_source == "web" else None,
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
