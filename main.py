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
    st.set_page_config(
        page_title="정권환 | AI Engineer Portfolio",
        page_icon="👋",
        layout="wide",
        initial_sidebar_state="auto",
    )

    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    # ── Sidebar ──────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔗 Contact")
        col_gh, col_li, col_mail = st.columns(3)
        col_gh.markdown(
            "[![GitHub](https://img.icons8.com/?size=32&id=fmFqQmR0UdsR&format=png)](https://github.com/ppijbb)"
        )
        col_li.markdown(
            "[![LinkedIn](https://img.icons8.com/?size=32&id=13930&format=png)](https://www.linkedin.com/in/권환-정-ba37b122b)"
        )
        col_mail.markdown(
            "[![Gmail](https://img.icons8.com/?size=32&id=37246&format=png)](mailto:ppijbb@gmail.com)"
        )
        st.markdown("---")
        st.caption("데이터 사이언티스트 / AI 엔지니어")

    # ── Hero Section ──────────────────────────────────────────────
    st.markdown(
        """
        <div style="padding: 2rem 0 1rem 0;">
            <h1 style="font-size:2.4rem; margin-bottom:0.2rem;">👋 안녕하세요, <span style="color:#F63366;">정권환</span>입니다.</h1>
            <p style="font-size:1.1rem; color:#555; margin-top:0.4rem;">
                헬스케어 · 디지털 바이오 · 음성/오디오 데이터 분야의 경험을 쌓고 있는<br>
                <strong>데이터 사이언티스트 &amp; AI 엔지니어</strong>입니다.
            </p>
            <p style="font-size:0.97rem; color:#777;">
                도메인과 목적에 맞게 설계된 AI 서비스를 연구하고 개발합니다.<br>
                데이터 분석 · 모델 아키텍처 · MLOps · LLM 서비스까지 폭넓게 다룹니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Main Content: two-column layout ──────────────────────────
    left_col, right_col = st.columns([1, 1], gap="large")

    # ── LEFT: Resume ─────────────────────────────────────────────
    with left_col:
        # EDUCATION
        st.markdown("### 🎓 Education")
        edu_data = [
            ("2011.03 – 2014.02", "노원 고등학교", ""),
            ("2014.03 – 2021.02", "가천대학교", "글로벌캠퍼스 컴퓨터공학과"),
            ("2025.03 – 재학 중", "성균관대학교", "데이터사이언스융합학과 석사과정"),
        ]
        for period, school, detail in edu_data:
            c1, c2 = st.columns([0.38, 0.62])
            c1.caption(period)
            c2.markdown(f"**{school}**")
            if detail:
                c2.caption(detail)

        st.markdown("---")

        # WORK EXPERIENCE
        st.markdown("### 💼 Work Experience")
        work_data = [
            ("2020.02 – 2020.06", "㈜휴레이포지티브", "기업부설연구소 인턴 연구원"),
            ("2020.09 – 2020.12", "행정안전부", "한국정보화진흥원 직접사업팀 인턴"),
            ("2021.04 – 2024.05", "㈜튜링바이오", "연구소 연구원 → 선임 연구원"),
            ("2024.06 – 현재", "㈜덴컴", "연구소 연구원"),
        ]
        for period, company, role in work_data:
            c1, c2 = st.columns([0.38, 0.62])
            c1.caption(period)
            c2.markdown(f"**{company}**")
            c2.caption(role)

        st.markdown("---")

        # AWARDS & CERTIFICATION
        aw_col, cert_col = st.columns(2)
        with aw_col:
            st.markdown("### 🏆 Awards")
            st.caption("2023.09 – 2023.10")
            st.markdown("**분당서울대학교병원**")
            st.caption("SNUBH-AWS ICU Datathon 4등상")

        with cert_col:
            st.markdown("### 📜 Certifications")
            st.caption("2018.06")
            st.markdown("**네트워크 관리사 2급**")
            st.caption("한국정보통신자격협회")
            st.caption("2019.10")
            st.markdown("**빅데이터분석 실무 2급**")
            st.caption("한국정보인재개발원")

        st.markdown("---")

        # SKILLS
        st.markdown("### 🛠️ Skills")
        st.html(
            """
<div style="font-family:'Roboto',sans-serif; font-size:14px; line-height:2.0;">
  <b>Language</b><br>
  <img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white">
  <br><b>Database</b><br>
  <img src="https://img.shields.io/badge/DynamoDB-4053D6?style=flat-square&logo=amazondynamodb&logoColor=white">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white">
  <br><b>Backend</b><br>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white">
  <br><b>Data Science</b><br>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white">
  <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white">
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white">
  <br><b>Deep Learning</b><br>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white">
  <img src="https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=keras&logoColor=white">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white">
  <br><b>LLM / MLOps</b><br>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white">
  <img src="https://img.shields.io/badge/HuggingFace-FF9A00?style=flat-square&logo=huggingface&logoColor=white">
  <img src="https://img.shields.io/badge/Ray-028CF0?style=flat-square&logo=ray&logoColor=white">
  <br><b>Infrastructure</b><br>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white">
  <img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white">
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white">
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/WebRTC-333333?style=flat-square&logo=webrtc&logoColor=white">
</div>
            """
        )

    # ── RIGHT: Projects ───────────────────────────────────────────
    with right_col:
        st.markdown("### 🔬 Healthcare / Bioinformatics")
        st.page_link(
            "pages/cardio.py",
            label="🫀 심혈관계 질환자 180명 다중 오믹스 데이터 분석",
        )
        st.page_link(
            "pages/dep_peptide.py",
            label="🧬 우울장애 218명 펩타이드 분석 · 바이오마커 후보 추출",
        )
        st.page_link(
            "pages/dep_scales.py",
            label="📊 우울장애 의사진단 · 자가진단 데이터 상관관계 분석",
        )
        st.page_link(
            "pages/sleep_challenge.py",
            label="😴 분당서울대병원 수면 인공지능 경진대회",
        )
        st.page_link(
            "pages/icu_challenge.py",
            label="🏥 분당서울대병원 COVID-19 중환자 데이터톤 (SNUBH-AWS)",
        )

        st.markdown("### 🤖 LLM / NLP Services")
        st.page_link(
            "pages/llm_app.py",
            label="💬 NLP 기반 우울장애 중증도 평가 LLM 챗봇 (Schema GPT)",
        )
        st.page_link(
            "pages/qdrant_vdb.py",
            label="🔗 Advanced RAG 챗봇 (Qdrant + Multi-Query + BM25)",
        )
        st.page_link(
            "pages/chat_guard.py",
            label="🛡️ LLM 챗봇 서비스 Prompt Injection Guard",
        )
        st.page_link(
            "pages/llm_tokenizing.py",
            label="📎 오픈소스 LLM 토큰 계산기",
        )

        st.markdown("### 👁️ Computer Vision / Audio")
        st.page_link(
            "pages/facial.py",
            label="😊 실시간 안면 감정인식 기반 감성 분석 엔진 (온디바이스 추론)",
        )
        st.page_link(
            "pages/zsd_organoid.py",
            label="🔭 실시간 Zero-Shot 이미지 Detection 서비스",
        )
        st.page_link(
            "pages/dtw_vectordb.py",
            label="🎵 음원 MFCC VectorDB (DTW 유사도 검색)",
        )
        st.page_link(
            "pages/ocr.py",
            label="🖼️ 공연 포스터 OCR 데이터 수집 (EasyOCR / PaddleOCR)",
        )

        st.markdown("### 🧰 Toy Projects")
        st.page_link(
            "pages/shop_search.py",
            label="🐾 애견 관련 기업 정보 웹 스크래핑",
        )
        st.page_link(
            "pages/concert_search.py",
            label="🎤 실시간 공연 정보 수집 · 자동 검색",
        )
        st.page_link(
            "pages/rtc_call.py",
            label="📞 WebRTC 기반 다인원 음성 채팅",
        )
        st.page_link(
            "pages/slack.py",
            label="🤖 SlackBot 구현",
        )
