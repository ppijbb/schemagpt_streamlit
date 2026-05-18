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


_PROFILE_CSS = """
<style>
/* ── 전체 페이지 배경 ── */
.main .block-container { padding-top: 1.5rem; }

/* ── 히어로 카드 ── */
.hero-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    color: #ffffff;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.hero-card h1 { font-size: 2.2rem; margin-bottom: 0.3rem; }
.hero-card .subtitle {
    font-size: 1.05rem;
    color: #a8d8ea;
    line-height: 1.7;
    margin-bottom: 1rem;
}
.hero-card .tag {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.8rem;
    margin: 0.2rem 0.2rem 0 0;
    backdrop-filter: blur(4px);
}

/* ── 섹션 헤더 ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f3460;
    border-left: 4px solid #e94560;
    padding-left: 0.6rem;
    margin: 1.4rem 0 0.8rem 0;
    letter-spacing: 0.03em;
}

/* ── 타임라인 아이템 ── */
.timeline-item {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 0.75rem;
    align-items: flex-start;
}
.timeline-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #e94560;
    margin-top: 0.45rem;
    flex-shrink: 0;
}
.timeline-year {
    font-size: 0.78rem;
    color: #888;
    white-space: nowrap;
    min-width: 100px;
    padding-top: 0.1rem;
}
.timeline-content { font-size: 0.9rem; line-height: 1.5; }
.timeline-content strong { color: #1a1a2e; }
.timeline-content small { color: #666; display: block; }

/* ── 프로젝트 카드 ── */
.project-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem; }
.project-tag {
    background: #f0f4ff;
    border: 1px solid #d0d9f0;
    border-radius: 8px;
    padding: 0.4rem 0.75rem;
    font-size: 0.82rem;
    color: #0f3460;
    cursor: default;
    transition: background 0.2s;
}
.project-tag:hover { background: #dce6ff; }

/* ── 기술 스택 배지 래퍼 ── */
.badge-section { margin-bottom: 0.4rem; }
.badge-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
}
.badge-row { display: flex; flex-wrap: wrap; gap: 0.35rem; }

/* ── 수상/자격 카드 ── */
.award-card {
    background: linear-gradient(90deg, #fff8e1, #ffffff);
    border-left: 4px solid #f9a825;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
}
.award-card .award-title { font-weight: 700; color: #333; }
.award-card .award-sub { color: #777; font-size: 0.8rem; }

.cert-card {
    background: linear-gradient(90deg, #e8f5e9, #ffffff);
    border-left: 4px solid #43a047;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
}
.cert-card .cert-title { font-weight: 700; color: #333; }
.cert-card .cert-sub { color: #777; font-size: 0.8rem; }

/* ── 사이드바 소셜 버튼 ── */
.social-row { display: flex; gap: 0.5rem; justify-content: center; margin-top: 0.5rem; }
.social-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #f0f4ff;
    border: 1px solid #cdd5f0;
    border-radius: 8px;
    padding: 0.4rem 0.7rem;
    font-size: 0.8rem;
    color: #0f3460;
    text-decoration: none;
    transition: background 0.2s;
}
.social-btn:hover { background: #dce6ff; }

/* ── Streamlit 기본 요소 튜닝 ── */
[data-testid="stSidebar"] { background: #f8f9fc; }
a { color: inherit; }
</style>
"""


def _badge(name: str, color: str, logo: str, logo_color: str = "white") -> str:
    return (
        f'<img src="https://img.shields.io/badge/{name}-{color}'
        f'?style=flat-square&logo={logo}&logoColor={logo_color}" '
        f'style="height:22px; margin:2px;">'
    )


def _timeline(year: str, title: str, subtitle: str = "") -> str:
    sub_html = f"<small>{subtitle}</small>" if subtitle else ""
    return f"""
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <span class="timeline-year">{year}</span>
        <div class="timeline-content"><strong>{title}</strong>{sub_html}</div>
    </div>"""


def _award(title: str, sub: str) -> str:
    return f"""
    <div class="award-card">
        <div class="award-title">🏆 {title}</div>
        <div class="award-sub">{sub}</div>
    </div>"""


def _cert(title: str, sub: str) -> str:
    return f"""
    <div class="cert-card">
        <div class="cert-title">📜 {title}</div>
        <div class="cert-sub">{sub}</div>
    </div>"""


if __name__ == "__main__":
    st.set_page_config(
        page_title="정권환 | AI Portfolio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.markdown(_PROFILE_CSS, unsafe_allow_html=True)

    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    # ── 사이드바 ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 정권환")
        st.caption("AI Engineer · Data Scientist")
        st.markdown(
            """
            <div class="social-row">
              <a class="social-btn" href="https://github.com/ppijbb" target="_blank">
                <img src="https://img.icons8.com/?size=18&id=fmFqQmR0UdsR&format=png"> GitHub
              </a>
              <a class="social-btn" href="https://www.linkedin.com/in/권환-정-ba37b122b" target="_blank">
                <img src="https://img.icons8.com/?size=18&id=13930&format=png"> LinkedIn
              </a>
              <a class="social-btn" href="mailto:ppijbb@gmail.com">
                <img src="https://img.icons8.com/?size=18&id=37246&format=png"> Email
              </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown("**🔗 프로젝트 바로가기**")
        st.page_link("pages/cardio.py",         label="심혈관계 다중 오믹스 분석")
        st.page_link("pages/dep_peptide.py",    label="우울장애 펩타이드 분석")
        st.page_link("pages/dep_scales.py",     label="우울 자가진단 상관관계")
        st.page_link("pages/facial.py",         label="안면 감정인식 엔진")
        st.page_link("pages/llm_app.py",        label="심리 상담 LLM 챗봇")
        st.page_link("pages/qdrant_vdb.py",     label="Advanced RAG 챗봇")
        st.page_link("pages/llm_tokenizing.py", label="LLM 토큰 계산기")
        st.page_link("pages/chat_guard.py",     label="Prompt Guard")

    # ── 히어로 섹션 ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-card">
          <h1>👋 안녕하세요, 정권환입니다</h1>
          <div class="subtitle">
            헬스케어 · 디지털 바이오 · 음성/오디오 분야를 중심으로<br>
            데이터 과학부터 LLM 서비스까지 도메인에 맞는 AI를 연구·개발합니다.
          </div>
          <span class="tag">Healthcare AI</span>
          <span class="tag">LLM / RAG</span>
          <span class="tag">MLOps</span>
          <span class="tag">NLP</span>
          <span class="tag">Computer Vision</span>
          <span class="tag">Bioinformatics</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPI 메트릭 ────────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("경력", "4 + yr", help="㈜튜링바이오, ㈜덴컴")
    m2.metric("프로젝트", "17 +", help="헬스케어·LLM·CV 등")
    m3.metric("대학원", "재학 중", help="성균관대 데이터사이언스융합 석사")
    m4.metric("수상", "ICU Datathon 4위", help="분당서울대병원 2023")

    st.markdown("---")

    # ── 메인 2컬럼 ───────────────────────────────────────────────────────────
    left, right = st.columns([0.42, 0.58], gap="large")

    # ───── 왼쪽: 학력 · 경력 · 수상 · 자격 ─────────────────────────────────
    with left:
        # 학력
        st.markdown('<div class="section-header">🎓 EDUCATION</div>', unsafe_allow_html=True)
        st.markdown(
            _timeline("2011.03 – 2014.02", "노원 고등학교")
            + _timeline("2014.03 – 2021.02", "가천대학교", "글로벌캠퍼스 컴퓨터공학과")
            + _timeline("2025.03 – 재학 중", "성균관대학교", "데이터사이언스융합학과 석사과정"),
            unsafe_allow_html=True,
        )

        # 경력
        st.markdown('<div class="section-header">💼 WORK EXPERIENCE</div>', unsafe_allow_html=True)
        st.markdown(
            _timeline("2020.02 – 2020.06", "㈜휴레이포지티브", "기업부설연구소 인턴 연구원")
            + _timeline("2020.09 – 2020.12", "행정안전부", "한국정보화진흥원 직접사업팀 인턴")
            + _timeline("2021.04 – 2024.05", "㈜튜링바이오", "연구소 연구원 → 선임 연구원")
            + _timeline("2024.06 – 현재", "㈜덴컴", "연구소 연구원"),
            unsafe_allow_html=True,
        )

        # 수상
        st.markdown('<div class="section-header">🏆 AWARDS</div>', unsafe_allow_html=True)
        st.markdown(
            _award(
                "SNUBH-AWS ICU Datathon 4등상",
                "분당서울대병원 · 2023.09 – 2023.10",
            ),
            unsafe_allow_html=True,
        )

        # 자격증
        st.markdown('<div class="section-header">📜 CERTIFICATIONS</div>', unsafe_allow_html=True)
        st.markdown(
            _cert("네트워크 관리사 2급", "한국정보통신자격협회 · 2018.06")
            + _cert("빅데이터분석 실무 2급", "한국정보인재개발원 · 2019.10"),
            unsafe_allow_html=True,
        )

    # ───── 오른쪽: 프로젝트 · 기술 스택 ──────────────────────────────────────
    with right:
        # 프로젝트
        st.markdown('<div class="section-header">👨‍💻 PROJECTS</div>', unsafe_allow_html=True)

        _PROJECTS = [
            ("pages/cardio.py",         "🫀 심혈관계 질환자 180명 다중 오믹스 데이터 분석",           "헬스케어"),
            ("pages/dep_peptide.py",    "🧬 우울장애 218명 펩타이드 분석 및 바이오마커 후보 추출",      "헬스케어"),
            ("pages/dep_scales.py",     "📊 우울장애 의사진단 · 자가진단 상관관계 분석",               "헬스케어"),
            ("pages/facial.py",         "😊 실시간 안면 감정인식 기반 감성 분석 엔진",                  "CV"),
            ("pages/llm_app.py",        "🤖 Schema Therapy 기반 우울장애 심리 상담 챗봇",              "LLM"),
            ("pages/sleep_challenge.py","😴 분당서울대병원 수면 AI 경진대회",                           "헬스케어"),
            ("pages/icu_challenge.py",  "🏥 COVID-19 중환자 데이터톤",                                "헬스케어"),
            ("pages/zsd_organoid.py",   "🔬 실시간 Zero-shot 이미지 Detection 서비스",                "CV"),
            ("pages/dtw_vectordb.py",   "🎵 음원 MFCC VectorDB (DTW 유사도 검색)",                   "MLOps"),
            ("pages/qdrant_vdb.py",     "📚 Advanced RAG 챗봇 (Qdrant + Multi-Query + BM25)",         "LLM"),
            ("pages/llm_tokenizing.py", "🔢 오픈소스 · ChatGPT LLM 토큰 계산기",                      "LLM"),
            ("pages/chat_guard.py",     "🛡️ LLM 챗봇 Prompt Guard (OpenVINO CPU Inference)",         "MLOps"),
            ("pages/shop_search.py",    "🐶 애견 관련 기업 정보 수집 (toy)",                           "Toy"),
            ("pages/ocr.py",            "🎭 공연 포스터 OCR 데이터 수집 (toy)",                        "Toy"),
            ("pages/concert_search.py", "🎶 실시간 공연 정보 수집 · 자동 검색 (toy)",                  "Toy"),
            ("pages/rtc_call.py",       "🎙️ WebRTC 기반 다인원 음성 채팅 (toy)",                      "Toy"),
            ("pages/slack.py",          "💬 SlackBot 만들기 (toy)",                                    "Toy"),
        ]

        _TAG_COLOR = {
            "헬스케어": "#e8f4fd",
            "LLM":     "#f3e8fd",
            "CV":      "#e8fdf0",
            "MLOps":   "#fdf3e8",
            "Toy":     "#fdf8e8",
        }
        _TAG_TEXT = {
            "헬스케어": "#1565c0",
            "LLM":     "#6a1b9a",
            "CV":      "#1b5e20",
            "MLOps":   "#e65100",
            "Toy":     "#795548",
        }

        for page, label, tag in _PROJECTS:
            c1, c2 = st.columns([0.85, 0.15])
            with c1:
                st.page_link(page, label=label)
            with c2:
                bg = _TAG_COLOR.get(tag, "#eee")
                tc = _TAG_TEXT.get(tag, "#333")
                st.markdown(
                    f'<span style="background:{bg};color:{tc};border-radius:6px;'
                    f'padding:2px 7px;font-size:0.72rem;font-weight:600;">{tag}</span>',
                    unsafe_allow_html=True,
                )

        # 기술 스택
        st.markdown('<div class="section-header">⚙️ SKILLS</div>', unsafe_allow_html=True)

        _SKILL_GROUPS = {
            "Language": [
                ("python-3776AB",  "python",      "white"),
                ("R-276DC3",       "r",           "black"),
            ],
            "Database": [
                ("DynamoDB-4053D6",  "amazondynamodb", "white"),
                ("MySQL-4479A1",     "mysql",          "white"),
                ("PostgreSQL-003545","postgresql",     "white"),
                ("MongoDB-47A248",   "mongodb",        "white"),
            ],
            "Backend": [
                ("FastAPI-009688",  "fastapi", "white"),
                ("Flask-000000",    "flask",   "white"),
                ("Django-092E20",   "django",  "white"),
            ],
            "Data Science": [
                ("scikit--learn-F7931E","scikitlearn","black"),
                ("NumPy-013243",        "numpy",      "black"),
                ("Pandas-150458",       "pandas",     "black"),
                ("Plotly-3F4F75",       "plotly",     "black"),
            ],
            "Deep Learning": [
                ("PyTorch-EE4C2C",    "pytorch",    "black"),
                ("TensorFlow-FF6F00", "tensorflow", "black"),
                ("Keras-D00000",      "keras",      "black"),
                ("OpenCV-5C3EE8",     "opencv",     "black"),
            ],
            "LLM / AI": [
                ("LangChain-1C3C3C",  "langchain",   "white"),
                ("OpenAI-412991",     "openai",      "black"),
                ("HuggingFace-FF9A00","huggingface", "white"),
            ],
            "Cloud / Infra": [
                ("AWS-232F3E",      "amazonaws", "white"),
                ("GCP-4285F4",      "googlecloud","white"),
                ("Docker-2496ED",   "docker",    "black"),
                ("Linux-FCC624",    "linux",     "black"),
            ],
            "Version Control": [
                ("GitHub-181717", "github", "white"),
                ("Git-F05032",    "git",    "white"),
            ],
        }

        for group, items in _SKILL_GROUPS.items():
            badges = "".join(_badge(n, c, lo, lc) for n, c, lo, lc in items)
            st.markdown(
                f'<div class="badge-section">'
                f'<div class="badge-label">{group}</div>'
                f'<div class="badge-row">{badges}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
