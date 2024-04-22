import string

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from srcs.facial import VideoProcessor, AudioProcessor
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
        
            고령호발질환 예측 및 진단 시스템 실증 및 실용화 연구 연계 연구
            얼굴 감정, 발화 감정, 문진 점수를 종합적으로 평가하는 App
            과제 최종 평가 A등급, 울산대 후원 부울경 스타트업 IR 데모데이 최우수상 수상


        ## 개발 내용
        - 우울증 채팅 문진 진행 중 발화자의 감정을 추적하여 정확한 상태 평가를 진행하는 App 개발
        - LLM, NLP(Natural Language Process) 모델, 얼굴 감정 인식 모델 연구 및 개발
        - ML 서비스를 위한 FastAPI 백엔드 개발 및 AWS EC2 인스턴스 관리
        ### NLP
        - 채팅 중 문진 진행 및 평가를 위한 룰베이스 채팅 프로세스 기획
        - 자연어 분석을 통한 채팅 프로세스 목적에 맞는 8개 task Finetuning 모델 학습
              감성 분류
              문진 응답 평가
              우울 키워드 분류
              응답 발화 생성
              문진 질문 생성
              STS 텍스트 임베딩
              발화 이해를 위한 NLI
              문장 감성 레벨 평가 모델
        - 초기 학습한 문진 질문 생성 모델과 응답 발화 생성 모델은 LLM에서 처리하도록 수정
        - 우울 문진에 적합한 채팅을 할 수 있는 Prompt Engineering
        ### Image Processing
        - 얼굴 감정 데이터 50만 건 중 서비스에 필요한 데이터 20만 건 
        - 원천 데이터는 App에서 입력받는 영상의 형태와 다르기 때문에 데이터에서 얼굴 위치만 crop
        - 해당 모델은 실시간으로 분석을 해야하기 때문에 경량모델 MobilNetV3로 학습
        - 학습 데이터에 대한 Acc 85%
        ### BackEnd
        - 데이터는 MySQL DB에 저장
        - 채팅 종료 시점에 얼굴 감정 데이터 DB에 입력
        - 얼굴 감정인식은 모바일에서 이뤄지지 않고 WebRTC를 통해 웹뷰에서 처리
 

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
