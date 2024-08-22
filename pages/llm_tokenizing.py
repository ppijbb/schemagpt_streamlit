import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from srcs.st_cache import get_or_create_eventloop, get_llm_tokenizer




if __name__ == "__main__":
    st.set_page_config(page_title="tokenizing",
                       page_icon="📎",
                       layout="wide",
                       initial_sidebar_state="auto",)
    tokenizer_map = get_llm_tokenizer()
    st.title('📎 LLM Token Calculator')

    st.markdown('''
                
        ## 프로젝트 소개
        
            오픈소스 LLM 토큰 수 계산기


        ## 개발 내용
        - 오픈 소스별 토큰 수 계산
 

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        ''', unsafe_allow_html=True)
    st.markdown("---")
    text = st.text_area(label="Enter text",
                        value="The quick brown fox jumps over the lazy dog.")
    if st.button(label="Calculate"):
        st.write("Number of characters:", len(text))
        for name, tokenizer in tokenizer_map.items():
            tokens = tokenizer.tokenize(text)
            st.write(f"{name}'s tokens : {len(tokens)}")
