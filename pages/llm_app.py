import asyncio
import copy
import streamlit as st
import torch

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_openai import ChatOpenAI

from srcs import schema_therapy
from srcs.graph.agent_common import (
    build_search_tools,
    create_search_agent,
    invoke_agent,
)
from srcs.st_cache import get_utterance_data

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    st.set_page_config(page_title="chat app",
                       page_icon="🤖",
                       layout="wide",
                       initial_sidebar_state="auto",)
    vector_db = get_utterance_data()
    st.title('🤖 LLM based Chatbot App')
    st.markdown('''

            ## 프로젝트 소개

                Schema therapy 기반 심리 상담 챗봇
                RAG + ReAct 심리도식 분석으로 우울감의 원인 추론
                               

            ## 개발 내용
            - 우울증 채팅 문진 진행 중 발화자의 감정을 추적하여 정확한 상태 평가를 진행하는 App 개발
            - LLM, NLP(Natural Language Process) 모델, 얼굴 감정 인식 모델 연구 및 개발
            - ML 서비스를 위한 FastAPI 백엔드 개발 및 AWS EC2 인스턴스 관리
            
            ### NLP
            - 채팅 중 사용자 발화의 심리도식 분석을 위한 룰베이스 채팅 프로세스 기획
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
            - 우울 문진에 적합한 채팅을 할 수 있는 Prompt Engineering + Fine tuning
            - 현재 버전에서는 LangGraph 기반 ReAct agent 사용
            
            ### BackEnd
            - MySQL DB 사용
            - FastAPI + Gunicorn 백엔드 개발 및 서비스
            - AWS 클라우드 아키텍처 설계


            ## 사용 기술
            <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
            <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
            <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
            <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
            <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=black"> 
            ''', unsafe_allow_html=True)
    st.image("pages/image/llm_app/architecture.jpg")

    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    with st.sidebar:
        try:
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    CHAT_MAX_MESSAGES = 21

    st.title("Langchain Version")
    col1, col2 = st.columns(2)

    with col1:
        st.title("🔎 DDG GPT")
        st.caption("DuckDuckGo 검색 엔진을 통한 응답")
        col1_chat_container = st.container()
        msgs = StreamlitChatMessageHistory()
        if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
            msgs.clear()
            msgs.add_message(SystemMessage(content="검색 결과를 보고 종합적 정보만 요약해 전달하세요."))
            msgs.add_ai_message("무엇을 알려드릴까요?")
        avatars = {"human": "user", "ai": "assistant", "system": "system"}
        for msg in msgs.messages:
            if msg.type != "system":
                with col1_chat_container.chat_message(avatars[msg.type]):
                    st.write(msg.content)

        if prompt := col1.chat_input(placeholder="경복궁의 위치는?", key=col1):
            col1_chat_container.chat_message("user").write(prompt)
            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()
            llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, temperature=0)
            tools = build_search_tools(include_arxiv=True, ddg_max_results=10)
            agent = create_search_agent(llm, tools)
            history = list(msgs.messages)[-(CHAT_MAX_MESSAGES - 1) :] + [
                HumanMessage(content=prompt)
            ]
            try:
                response_text = invoke_agent(agent, history)
                msgs.add_user_message(prompt)
                msgs.add_ai_message(response_text)
                if len(msgs.messages) > CHAT_MAX_MESSAGES:
                    system_msgs = [m for m in msgs.messages if getattr(m, "type", None) == "system"]
                    rest = [
                        m
                        for m in msgs.messages
                        if getattr(m, "type", None) != "system"
                    ][-(CHAT_MAX_MESSAGES - len(system_msgs)) :]
                    msgs.messages = system_msgs + rest
                col1_chat_container.chat_message("assistant").write(response_text)
            except Exception as e:
                st.toast(f"An error occurred: {e}")

    with col2:
        st.title("🤸 Schema GPT")
        st.caption("Schema Therapy 기반 정신 건강 챗봇")
        col2_chat_container = st.container()
        if "messages2" not in st.session_state:
            st.session_state["messages2"] = [
                {"role": "system", "content": schema_therapy.system_prompt},
                {"role": "assistant", "content": "안녕하세요. 오늘 하루는 어떠셨나요?"},
            ]

        for msg in st.session_state.messages2:
            if msg["role"] != "system":
                col2_chat_container.chat_message(msg["role"]).write(msg["content"])

        if col2_prompt := col2.chat_input(placeholder="지치고 힘들어요", key=col2):
            st.session_state.messages2.append({"role": "user", "content": col2_prompt})
            col2_chat_container.chat_message("user").write(col2_prompt)
            with torch.inference_mode():
                searched_result = vector_db.invoke(col2_prompt)[0]
                maladaptive_schema = schema_therapy.MAL_IDS[searched_result.metadata["maladaptive"]]

            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key, temperature=0)
            tools = build_search_tools(
                include_arxiv=True,
                ddg_max_results=20,
                ddg_time="d",
            )
            agent = create_search_agent(llm, tools)
            search_instruction = copy.deepcopy(st.session_state.messages2)
            search_instruction[-1]["content"] += f"\n(심리도식 [{maladaptive_schema}])"
            try:
                response_text = invoke_agent(agent, search_instruction)
                st.session_state.messages2.append({"role": "assistant", "content": response_text})
                if len(st.session_state.messages2) > CHAT_MAX_MESSAGES:
                    system_msg = next(
                        (m for m in st.session_state.messages2 if m["role"] == "system"), None
                    )
                    rest = [
                        m
                        for m in st.session_state.messages2
                        if m["role"] != "system"
                    ][-(CHAT_MAX_MESSAGES - 1) :]
                    st.session_state.messages2 = ([system_msg] if system_msg else []) + rest
                col2_chat_container.chat_message("assistant").write(response_text)
            except Exception as e:
                st.toast(f"An error occurred: {e}")
