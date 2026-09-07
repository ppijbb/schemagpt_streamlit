from typing import List
import uuid

import streamlit as st
from streamlit_webrtc import webrtc_streamer, create_mix_track, WebRtcMode, WebRtcStreamerContext
from streamlit_server_state import server_state, server_state_lock

from srcs.rtc_call import VideoProcessor, AudioProcessor, process_face
from pages.rtc.config import RTC_CONFIGURATION


if 'room_id' not in st.session_state:
    st.session_state.room_id = uuid.uuid4().hex


def show(key:str, track=None):
    # When needed: queries = st.query_params; code = queries.get("code", [None])[0]
    webrtc_ctx = webrtc_streamer(
        key=key,
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
        # video_processor_factory=VideoProcessor,
        source_audio_track=track,
        source_video_track=track,
        video_processor_factory=None,
        audio_processor_factory=AudioProcessor,
        async_processing=True,
        desired_playing_state=None,
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
        webrtc_ctx.audio_processor.code = None
    
    if webrtc_ctx.input_video_track and track is not None:
        track.add_input_track(webrtc_ctx.input_video_track)

    with server_state_lock["webrtc_contexts"]:
        webrtc_contexts: List[WebRtcStreamerContext] = server_state["webrtc_contexts"]
        self_is_playing = webrtc_ctx.state.playing
        if self_is_playing and webrtc_ctx not in webrtc_contexts:
            webrtc_contexts.append(webrtc_ctx)
            server_state["webrtc_contexts"] = webrtc_contexts
        elif not self_is_playing and webrtc_ctx in webrtc_contexts:
            webrtc_contexts.remove(webrtc_ctx)
            server_state["webrtc_contexts"] = webrtc_contexts

    # Audio streams are transferred in SFU manner
    # TODO: Create MCU to mix audio streams
    for ctx in webrtc_contexts:
        if ctx == webrtc_ctx or not ctx.state.playing:
            continue
        webrtc_streamer(
            key=f"sound-{id(ctx)}",
            mode=WebRtcMode.RECVONLY,
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={"video": False, "audio": True},
            source_audio_track=ctx.input_audio_track,
            desired_playing_state=ctx.state.playing,
        )



if __name__ == "__main__":
    st.set_page_config(page_title="RTC Multi call",
                       page_icon="☎️",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('😄😑😭 Stream Call')
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
    with server_state_lock["rooms"]:
        if "rooms" not in server_state:
            server_state["rooms"] = []

    rooms = server_state["rooms"] + [st.session_state.room_id,]

    room_list, room_setting = st.columns(2)
    with room_list:
        room = st.sidebar.radio(label="Select room", options=rooms, key="room_list")
        if st.button("create new chat"):
            st.session_state.room_id = uuid.uuid4().hex
            rooms += [st.session_state.room_id]
    with room_setting:
        with st.sidebar.form("New room"):

            def on_create():
                new_room_name = st.session_state.new_room_name
                with server_state_lock["rooms"]:
                    server_state["rooms"] = server_state["rooms"] + [new_room_name]

            st.text_input(label="Room name", key="new_room_name")
            st.form_submit_button("Create a new room", on_click=on_create)

        if not room:
            st.stop()

    room_key = f"room_{room}"
    with server_state_lock[room_key]:
        if room_key not in server_state:
            server_state[room_key] = []

    if room is not None:
        st.session_state.room_id = room
    st.text_input("입장할 Room ID", key="room_id")
    
    with server_state_lock["webrtc_contexts"]:
        if "webrtc_contexts" not in server_state:
            server_state["webrtc_contexts"] = []

    with server_state_lock["mix_track"]:
        if "mix_track" not in server_state:
            server_state["mix_track"] = create_mix_track(
                kind="video", mixer_callback=process_face, key="mix"
            )

    show(key=st.session_state.room_id,
         track=server_state["mix_track"])
