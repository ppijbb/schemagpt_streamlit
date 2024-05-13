# __import__('pysqlite3')
import os
import asyncio
import sys
import copy
import signal
import time
import json
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "1"
# os.environ["TOKENIZERS_PARALLELISM"] = "0"

# from srcs.app_static_file_handler import AppStaticFileHandler

# sys.modules["streamlit.web.server.app_static_file_handler"].AppStaticFileHandler = AppStaticFileHandler

import pandas as pd
import streamlit as st

from langchain.callbacks.manager import CallbackManager
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType, ConversationalChatAgent, AgentExecutor, Tool
from langchain.agents.loading import AGENT_TO_CLASS, load_agent
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.tools import DuckDuckGoSearchRun, BingSearchRun, WikipediaQueryRun
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import (DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper, BingSearchAPIWrapper,
                                           SerpAPIWrapper, WikipediaAPIWrapper, PubMedAPIWrapper)
# from langchain_community.utilities.pubmed import PubMedAPIWrapper

from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from langchain_openai import ChatOpenAI
from ionic_langchain.tool import IonicTool

from srcs import schema_therapy
from srcs.st_cache import get_utterance_data, get_or_create_eventloop


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
                RAG 적용 심리도식 기반 우울감의 원인 추론
                               

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

    st.title("Langchain Version")
    col1, col2 = st.columns(2)
    
    with col1:
        st.title("🔎 DDG GPT")
        """
        DuckDuckGo 검색 엔진을 통한 응답
        """
        col1_chat_container = st.container()
        msgs = StreamlitChatMessageHistory()
        memory = ConversationBufferMemory(chat_memory=msgs,
                                          return_messages=True,
                                          memory_key="chat_history",
                                          output_key="output")
        if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
            msgs.clear()
            msgs.add_message(SystemMessage(content="검색 결과를 보고 종합적 정보만 요약해 전달하세요."))
            msgs.add_ai_message("무엇을 알려드릴까요?")
            st.session_state.steps = {}
        avatars = {"human": "user", "ai": "assistant", "system": "system"}
        for idx, msg in enumerate(msgs.messages):
            if msg.type != "system":
                with col1_chat_container.chat_message(avatars[msg.type]):
                    # Render intermediate steps if any were saved
                    for step in st.session_state.steps.get(str(idx), []):
                        if step[0].tool == "_Exception":
                            continue
                        with st.status(f"**{step[0].tool}**: {step[0].tool_input}", state="complete"):
                            st.write(step[0].log)
                            st.write(step[1])
                    st.write(msg.content)

        if prompt := col1.chat_input(placeholder="경복궁의 위치는?", key=col1):
            col1_chat_container.chat_message("user").write(prompt)

            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                             openai_api_key=openai_api_key,
                             streaming=True)
            tools = [
                DuckDuckGoSearchRun(
                    api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=10, 
                                                           region="en-en")),
                DuckDuckGoSearchRun(
                    api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=10, 
                                                           region="kr-kr")),
                WikipediaQueryRun(
                    api_wrapper=WikipediaAPIWrapper()),
                PubmedQueryRun(
                    api_wrapper=PubMedAPIWrapper()),
                IonicTool().tool()
                ] + load_tools(["arxiv"],)
            chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm,
                                                                    tools=tools)
            executor = AgentExecutor.from_agent_and_tools(agent=chat_agent,
                                                          tools=tools,
                                                          memory=memory,
                                                          max_iterations=3,
                                                          early_stopping_method="generate",
                                                          return_intermediate_steps=True,
                                                          handle_parsing_errors=True,)
            cfg = RunnableConfig()
            cfg["callbacks"] = [StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)]
            response = executor.invoke(prompt, cfg)
            st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]
            col1_chat_container.chat_message("assistant").write(response["output"])

    with col2:
        st.title("🤸 Schema GPT")
        """
        Schema Therapy 기반 정신 건강 챗봇 
        """
        col2_chat_container = st.container()
        if "messages2" not in st.session_state:
            st.session_state["messages2"] = [
                {
                    "role": "system",
                    "content": schema_therapy.system_prompt
                },
                {
                    "role": "assistant",
                    "content": "안녕하세요? 오늘 하루는 어떠셨나요?"
                }]

        for msg in st.session_state.messages2:
            if msg["role"] != "system":
                col2_chat_container.chat_message(msg["role"]).write(msg["content"])

        if col2_prompt := col2.chat_input(placeholder="지치고 힘들어요", key=col2):
            st.session_state.messages2.append(
                {
                    "role": "user",
                    "content": col2_prompt
                })
            col2_chat_container.chat_message("user").write(col2_prompt)
            searched_result = vector_db.similarity_search(col2_prompt)[0]
            maladaptive_schema = schema_therapy.MAL_IDS[searched_result.metadata["maladaptive"]]
            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            llm = ChatOpenAI(model_name="gpt-3.5-turbo",#"ft:gpt-3.5-turbo-0125:turingbio::93waZXFw",
                             openai_api_key=openai_api_key,
                             streaming=True)
            tools = [DuckDuckGoSearchRun(
                        api_wrapper=DuckDuckGoSearchAPIWrapper(time="d",
                                                               region="kr-kr",
                                                               max_results=20)),
                     DuckDuckGoSearchRun(
                        api_wrapper=DuckDuckGoSearchAPIWrapper(time="d",
                                                               region="en-en",
                                                               max_results=20)),
                     WikipediaQueryRun(
                        api_wrapper=WikipediaAPIWrapper()),
                     PubmedQueryRun(),
                     IonicTool().tool()] + load_tools(["arxiv"],)
            search_agent = initialize_agent(tools=tools,
                                            llm=llm,
                                            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                            # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                            handle_parsing_errors=True,
                                            max_iterations=5,
                                            early_stopping_method="generate",
                                            return_intermediate_steps=True,
                                            agent_kwargs={
                                                # "format_instructions": schema_therapy.format_instructions,
                                                "system_message_prefix": schema_therapy.prefix_prompt,
                                                "system_message_suffix": schema_therapy.suffix_prompt
                                                }
                                            # max_execution_time=15
                                            )
            # st.write(search_agent.agent.__dir__())

            # st.write(AGENT_TO_CLASS[AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION])
            # st.write(search_agent.agent.tool_run_logging_kwargs())
            with col2_chat_container.chat_message("assistant"):
                cfg = RunnableConfig()
                message_placeholder = st.empty()
                cfg["callbacks"] = [StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)]
                search_instruction = copy.deepcopy(st.session_state.messages2)
                search_instruction[-1]["content"] += f"\n(해당문장에 대한한 심리 도식 [{maladaptive_schema}] schema therapy strategy)"
                response = search_agent.invoke(search_instruction, cfg, chat_history=st.session_state.messages2)
                # st.write(response)
                output = json.loads(response["output"])["action_input"] if "{" in response["output"]  else response["output"]
                full_msg = ""
                for o in output:
                    full_msg += o
                    message_placeholder.markdown(f'{full_msg}▌')
                message_placeholder.markdown(full_msg)
                st.session_state.messages2.append(
                        {
                            "role": "assistant",
                            "content": output
                        })
