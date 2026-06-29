import asyncio
import copy
import streamlit as st

from langchain_openai import ChatOpenAI

from srcs.graph.agent_common import (
    build_search_tools,
    create_search_agent,
    invoke_agent,
)
from srcs.st_cache import get_audio_data


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    st.set_page_config(page_title="audio retriver app",
                       page_icon="🎼",
                       layout="wide",
                       initial_sidebar_state="auto",)
    vector_db = get_audio_data()
    st.title('🎼 Audio DTW DB App')
    st.markdown('''

            ## 프로젝트 소개

                chromadb 기반 audio mfcc dtw db
                유사 사운드 검색 
                               

            ## 개발 내용
            - ChromaDB 수정하여 custom embedding function, distance function 추가
            - 추가된 embedding function : 사운드 데이터 -> mfcc 로 저장
            - 추가된 distance function : mfcc -> dtw 를 score로 계산
            
            ### BackEnd
            - FastAPI + Gunicorn 백엔드 개발 및 서비스
            - Docker + goofys 통한 s3 데이터 처리


            ## 사용 기술
            <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
            <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
            <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
            <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">

            ''', unsafe_allow_html=True)

    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    with st.sidebar:
        # st.page_link("pages/cardio.py",)
        # st.page_link("pages/dep_peptide.py",)
        # st.page_link("pages/facial.py",)

        try:
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        except Exception as e:
                openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
                "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
                "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
                "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    CHAT_MAX_MESSAGES = 21

    st.title("Langchain Version")
    """
    MFCC-DTW 음원 검색
    """
    chat_container = st.container()
    st.file_uploader("검색하고 싶은 음악 스타일", type=["wav", "mp3"])
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "당신은 최신 음악을 추천해주는 GPT입니다."},
            {"role": "assistant", "content": "어떤 음악을 좋아하시나요?"},
        ]
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            chat_container.chat_message(msg["role"]).write(msg["content"])
    if st_prompt := st.chat_input(placeholder="슬플땐 힙합을 춰", key=st):
        st.session_state.messages.append({"role": "user", "content": st_prompt})
        chat_container.chat_message("user").write(st_prompt)
        searched_result = vector_db.invoke(st_prompt)[0]

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0)
        tools = build_search_tools(include_arxiv=True, ddg_max_results=20, ddg_time="d")
        agent = create_search_agent(llm, tools)
        search_instruction = copy.deepcopy(st.session_state.messages)
        search_instruction[-1]["content"] += "\n(최신 발매 음악 추천)"
        try:
            response_text = invoke_agent(agent, search_instruction)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            if len(st.session_state.messages) > CHAT_MAX_MESSAGES:
                system_msg = next(
                    (m for m in st.session_state.messages if m["role"] == "system"), None
                )
                rest = [m for m in st.session_state.messages if m["role"] != "system"][
                    -(CHAT_MAX_MESSAGES - 1) :
                ]
                st.session_state.messages = ([system_msg] if system_msg else []) + rest
            chat_container.chat_message("assistant").write(response_text)
        except Exception as e:
            st.toast(f"An error occurred: {e}")