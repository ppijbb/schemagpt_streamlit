import string

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from srcs.rtc_call import VideoProcessor, AudioProcessor
from pages.rtc.config import RTC_CONFIGURATION


def show():
    # queries = st.experimental_get_query_params()
    # code = queries.get("code", None)[0]
    webrtc_ctx = webrtc_streamer(
        key=string.punctuation,
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={
            "video": {
                # "frameRate": {
                #     "max": 60,
                #     "ideal": 0
                # },
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
        audio_processor_factory=AudioProcessor,
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
    st.set_page_config(page_title="facial emotion recognition",
                       page_icon="🫠",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('😄😑😭 Facial Emotion Recognition')
    st.markdown('''
                
        ## 프로젝트 소개
        
            모바일 채팅 및 음성 채팅을 위한 WebRTC 채널
            서버에 부담을 최소화하는 통신 연결 실험


        ## 개발 내용
        - 클라이언트 자원을 이용하는 채팅 및 음성 데이터 송수신 채널
        - 다화자 채팅 채널 구현
        - 채팅에 대한 봇 연결 검토
        ### NLP
        - 채팅 중 특정한 tool 을 동작시킬 수 있도록 Intent 분류 모델 검토
        - 실시간 부정 채팅 검수용 모델 검토

        ### Audio Processing
        - 오디오 효과 적용 
        - 오디오 로그 및 오디오 채팅 요약 검토
        - 불량 사용자 목소리에 대한 오디오 VectorDB 관리 검토
        ### BackEnd
        - Firebase 에서 서비스 실험
        - 서버 부하의 최소화 실험
 

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
        <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
        <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=black"> 
        <img src="https://img.shields.io/badge/keras-D00000?style=for-the-badge&logo=keras&logoColor=black"> 
        <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=black"> 
        ''', unsafe_allow_html=True)
    st.markdown("마이크와 웹캠을 이용합니다.")
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
