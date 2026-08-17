import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from srcs.st_cache import get_llm_tokenizer, get_tokenizer_model_ids


if __name__ == "__main__":
    st.set_page_config(
        page_title="tokenizing",
        page_icon="📎",
        layout="wide",
        initial_sidebar_state="auto",
    )
    model_ids = get_tokenizer_model_ids()
    st.title("📎 LLM Token Calculator")

    st.markdown(
        """
        ## 프로젝트 소개
            오픈소스 LLM 토큰 수 계산기
        ## 개발 내용
        - 오픈 소스별 토큰 수 계산
        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    TOKENIZER_COMPARE_MAX = 5

    if "tokenizer_compare_ids" not in st.session_state:
        st.session_state["tokenizer_compare_ids"] = []

    with st.sidebar:
        selected_id = st.selectbox("모델", options=model_ids, key="tokenizer_model_select")
        if st.button("비교할 모델로 추가"):
            if (
                selected_id not in st.session_state["tokenizer_compare_ids"]
                and len(st.session_state["tokenizer_compare_ids"]) < TOKENIZER_COMPARE_MAX
            ):
                st.session_state["tokenizer_compare_ids"].append(selected_id)
                st.rerun()
        if st.session_state["tokenizer_compare_ids"] and st.button("비교 목록 초기화"):
            st.session_state["tokenizer_compare_ids"] = []
            st.rerun()

    text = st.text_area(
        label="Enter text",
        value="The quick brown fox jumps over the lazy dog.",
        key="tokenizer_text",
    )
    if st.button(label="Calculate", key="tokenizer_calc_btn"):
        st.write("Number of characters:", len(text))
        ids_to_show = [selected_id] + [
            mid for mid in st.session_state["tokenizer_compare_ids"] if mid != selected_id
        ][:4]
        for model_id in ids_to_show:
            try:
                tokenizer = get_llm_tokenizer(model_id)
                tokens = tokenizer.tokenize(text)
                st.write(f"{model_id}'s tokens : {len(tokens)}")
            except Exception as e:
                st.write(f"{model_id}: error — {e}")
