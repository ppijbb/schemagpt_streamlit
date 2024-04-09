import string

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from srcs.facial import VideoProcessor
from pages.rtc.config import RTC_CONFIGURATION


st.set_page_config(page_title="facial emotion recognition",
                   page_icon="🫠",
                   layout="wide",
                   initial_sidebar_state="expanded",)


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
                    "max": 60,
                    "ideal": 0
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
            "autoPlay": True
        },
    )
    if webrtc_ctx.state.signalling:
        webrtc_ctx.video_processor.code = None


if __name__ == "__main__":
    st.title('😄😑😭 Facial Emotion Recognition')
    # with st.sidebar:
    #     st.page_link("pages/cardio.py",)
    #     st.page_link("pages/dep_peptide.py",)
    #     st.page_link("pages/facial.py",)
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
