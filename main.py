__import__('pysqlite3')
import asyncio
import os
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
os.environ["TOKENIZERS_PARALLELISM"] = "0"

from srcs.st_utils import AppStaticFileHandler

sys.modules["streamlit.web.server.app_static_file_handler"].AppStaticFileHandler = AppStaticFileHandler

import streamlit as st

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    st.set_page_config(page_title="main",
                    page_icon="👋",
                    layout="wide",
                    initial_sidebar_state="auto",)

    st.title('👋😄 Hello!')
    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    with st.sidebar:
        st.markdown("### 정권환")
        st.caption("Data Scientist · AI Engineer")
        st.divider()
        side1, side2, side3 = st.columns(3)
        side1.markdown("[![github](https://img.icons8.com/?size=24&id=fmFqQmR0UdsR&format=png)](https://github.com/ppijbb)")
        side2.markdown("[![LinkedIn](https://img.icons8.com/?size=24&id=13930&format=png)](https://www.linkedin.com/in/권환-정-ba37b122b)")
        side3.markdown("[![Gmail](https://img.icons8.com/?size=24&id=37246&format=png)](mailto:ppijbb@gmail.com)")
    
    st.markdown("""
      # 안녕하세요! 정권환입니다.

      헬스케어, 디지털 바이오, 음성/오디오 데이터 분야의 경험을 넓히고 있는
      
      데이터 사이언티스트, AI 엔지니어 입니다.

      데이터 분석, 모델 아키텍처, MLOps, LLM 서비스 등

      단순히 인공지능이 들어간 서비스가 아닌 도메인과 목적에 맞게 설계하고 연구합니다.

      상상만 하던 서비스를 만들어 내는 꿈을 가지고 개발하고 연구하고 있습니다.
      """)

    section1, section2 = st.columns(2)
    with section1:
      with st.container(border=True):
        st.markdown("### 🎓 EDUCATION")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2011.03~2014.02")
        inc.markdown("###### 노원 고등학교")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2014.03~2021.02")
        inc.markdown("###### 가천대학교")
        inc.markdown("글로벌 캠퍼스 컴퓨터공학과")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2025.03~ 재학 중")
        inc.markdown("###### 성균관대학교")
        inc.markdown("데이터사이언스융합학과 석사과정")

      with st.container(border=True):
        st.markdown("### 💻 WORK EXPERIENCE")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2020.02~2020.06")
        inc.markdown("###### ㈜휴레이포지티브")
        inc.markdown("기업부설연구소 인턴 연구원")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2020.09~2020.12")
        inc.markdown("###### 행정 안전부")
        inc.markdown("한국정보화진흥원 직접사업팀 인턴")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2021.04~2024.05")
        inc.markdown("###### ㈜튜링바이오")
        inc.markdown("연구소 연구원 → 선임 연구원")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2024.06~")
        inc.markdown("###### ㈜덴컴")
        inc.markdown("연구소 연구원")

      with st.container(border=True):
        st.markdown("### 🏆 AWARDS")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2023.09~2023.10")
        inc.markdown("###### 분당 서울대 병원")
        inc.markdown("SNUBH-AWS ICU Datathon 4등상")

      with st.container(border=True):
        st.markdown("### 📜 CERTIFICATION")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2018.06")
        inc.markdown("###### 네트워크 관리사 2급")
        inc.markdown("한국정보통신자격협회")
        years, inc = st.columns([0.4, 0.6])
        years.markdown("###### 2019.10")
        inc.markdown("###### 빅데이터분석 실무 2급")
        inc.markdown("한국정보인재개발원")

    with section2:
      st.markdown("### 👨‍🔧 PROJECTS")
      with st.expander("🏥 헬스케어 & 바이오 AI", expanded=True):
        st.page_link("pages/cardio.py", label="🔗 심혈관계 질환자 180명 다중 오믹스 데이터 분석")
        st.page_link("pages/dep_peptide.py", label="🔗 우울장애 218명 펩타이드 분석 및 바이오마커 후보 물질 추출")
        st.page_link("pages/dep_scales.py", label="🔗 우울장애 의사진단 데이터, 자가진단 데이터 상관관계 분석")
        st.page_link("pages/llm_app.py", label="🔗 NLP 기반 우울장애 중증도 평가 LLM 챗봇 서비스")
        st.page_link("pages/sleep_challenge.py", label="🔗 분당서울대학교병원 수면 인공지능 경진대회")
        st.page_link("pages/icu_challenge.py", label="🔗 분당서울대학교병원 COVID-19 중환자 데이터톤")
      with st.expander("🤖 LLM & RAG 서비스", expanded=True):
        st.page_link("pages/qdrant_vdb.py", label="🔗 Advanced RAG 챗봇 서비스")
        st.page_link("pages/llm_tokenizing.py", label="🔗 오픈소스 및 ChatGPT LLM 토큰 계산기")
        st.page_link("pages/chat_guard.py", label="🔗 LLM 챗봇 서비스를 위한 Prompt Guard")
      with st.expander("👁️ 비전 & 오디오", expanded=True):
        st.page_link("pages/facial.py", label="🔗 실시간 발화, 안면 감정인식 기반 감성 분석 엔진 학습 및 온디바이스 추론")
        st.page_link("pages/zsd_organoid.py", label="🔗 실시간 zero-shot 이미지 detection 서비스")
        st.page_link("pages/dtw_vectordb.py", label="🔗 음원 MFCC vectorDB")
      with st.expander("🧪 Toy Projects", expanded=False):
        st.page_link("pages/shop_search.py", label="🔗 애견 관련 기업 정보 수집 기능")
        st.page_link("pages/ocr.py", label="🔗 공연 포스터 OCR 데이터 수집 기능")
        st.page_link("pages/concert_search.py", label="🔗 실시간 공연 정보 수집 및 공연 정보 자동 검색 기능")
        st.page_link("pages/rtc_call.py", label="🔗 WebRTC 기반 다인원 음성 채팅")
        st.page_link("pages/slack.py", label="🔗 SlackBot 만들기")

      st.markdown("### 📚 SKILLS")
      st.markdown('''
  <div style="font-family:'Roboto'; font-size: 16px; font-weight: 400; color: black; font-weight: bold;">
    Language <br>
      <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
      <img src="https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=black"> 
    <br>
    Database<br>
      <img src="https://img.shields.io/badge/dynamodb-4053D6?style=for-the-badge&logo=0175C2&logoColor=white"> 
      <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
      <img src="https://img.shields.io/badge/postgresql-003545?style=for-the-badge&logo=postgresql&logoColor=white"> 
      <img src="https://img.shields.io/badge/mongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white">
  <!-- <img src="https://img.shields.io/badge/firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=white"> -->
    <br>
  <!--   Front<br>
      <img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black"> 
    <br> -->
    Back<br>
      <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
      <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
      <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">  
    <br>
    Data Science<br>
      <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=black"> 
      <img src="https://img.shields.io/badge/scipy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=black">
      <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
      <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=black"> 
      <img src="https://img.shields.io/badge/plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=black"> 
    <br>
    Deep Learning<br>
      <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=black"> 
      <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=black"> 
      <img src="https://img.shields.io/badge/keras-D00000?style=for-the-badge&logo=keras&logoColor=black"> 
      <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=black"> 
    <br>
    Version control <br>
      <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
      <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
      <img src="https://img.shields.io/badge/huggingface-FF9A00?style=for-the-badge&logo=huggingface&logoColor=white">
    <br>
    Environ<br>
      <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"> 
      <img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=black"> 
      <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=black"> 
    <br>
    Cloud<br>
      <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> 
      <img src="https://img.shields.io/badge/googlecloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"> 
    <br>
    Etc<br>
      <img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=black"> 
      <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=black"> 
      <img src="https://img.shields.io/badge/webrtc-333333?style=for-the-badge&logo=webrtc&logoColor=white">
    <br>
  </div>
      ''',
      unsafe_allow_html=True)
