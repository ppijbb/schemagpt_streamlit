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

from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from langchain_openai import ChatOpenAI
from ionic_langchain.tool import IonicTool

from srcs.st_cache import get_audio_data, get_or_create_eventloop


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

    st.title("Langchain Version")
    """
    MFCC-DTW 음원 검색
    """
    chat_container = st.container()
    st.file_uploader("검색하고 싶은 음악 스타일", type=["wav", "mp3"])
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": "당신은 최신 음악을 추천해주는 GPT입니다."
            },
            {
                "role": "assistant",
                "content": "어떤 음악을 좋아하시나요?"
            }]
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            chat_container.chat_message(msg["role"]).write(msg["content"])
    if st_prompt := st.chat_input(placeholder="슬플땐 힙합을 춰", key=st):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": st_prompt
            })
        chat_container.chat_message("user").write(st_prompt)
        searched_result = vector_db.get_relevant_documents(st_prompt)[0]

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
                                        # agent_kwargs={
                                            # "format_instructions": schema_therapy.format_instructions,
                                            # "system_message_prefix": schema_therapy.prefix_prompt,
                                            # "system_message_suffix": schema_therapy.suffix_prompt
                                            # }
                                        # max_execution_time=15
                                        )
        # st.write(search_agent.agent.__dir__())
        # st.write(AGENT_TO_CLASS[AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION])
        # st.write(search_agent.agent.tool_run_logging_kwargs())
        with chat_container.chat_message("assistant"):
            cfg = RunnableConfig()
            message_placeholder = st.empty()
            # cfg["callbacks"] = [StreamlitCallbackHandler(st.container(), 
            #                                              expand_new_thoughts=True)]
            search_instruction = copy.deepcopy(st.session_state.messages)
            search_instruction[-1]["content"] += f"\n(최신 발매 음악 추천)"
            response = search_agent.invoke(search_instruction, 
                                           cfg, 
                                           chat_history=st.session_state.messages)
            # st.write(response)
            output = json.loads(response["output"])["action_input"] if "{" in response["output"]  else response["output"]
            full_msg = ""
            for o in output:
                full_msg += o
                message_placeholder.markdown(f'{full_msg}▌')
            message_placeholder.markdown(full_msg)
            st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": output
                    })