__import__('pysqlite3')
import os
import asyncio
import sys
import copy
import signal
import time
import json
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "0"

from srcs.app_static_file_handler import AppStaticFileHandler

sys.modules["streamlit.web.server.app_static_file_handler"].AppStaticFileHandler = AppStaticFileHandler

import pandas as pd
import streamlit as st

from langchain.callbacks.manager import CallbackManager
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType, ConversationalChatAgent, AgentExecutor, Tool
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

st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded",)

vector_db = get_utterance_data()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    st.title('🤖 LLM based Chatbot App')
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

    col1, col2 = st.columns(2)

    with col1:
        st.title("🔎 Search with DuckDuckgo")
        """
        DuckDuckGo 검색을 통한 응답 
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
                    api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=2, 
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
                    "content": "안녕하세요? 어떤 이야기를 해볼까요?"
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

            llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0125:turingbio::93waZXFw",
                             openai_api_key=openai_api_key,
                             streaming=True)
            tools = [DuckDuckGoSearchRun(
                        api_wrapper=DuckDuckGoSearchAPIWrapper(time="d",
                                                               region="kr-kr",
                                                               max_results=5)),
                     WikipediaQueryRun(
                        api_wrapper=WikipediaAPIWrapper()),
                     PubmedQueryRun(),
                     IonicTool().tool()] + load_tools(["arxiv"],)
            search_agent = initialize_agent(tools=tools,
                                            llm=llm,
                                            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                            handle_parsing_errors=True,
                                            max_iterations=3,
                                            max_execution_time=15)
            with col2_chat_container.chat_message("assistant"):
                cfg = RunnableConfig()
                cfg["callbacks"] = [StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)]
                search_instruction = copy.deepcopy(st.session_state.messages2)
                search_instruction[-1]["content"] += f"\n(해당문장에서 비롯된 심리 도식 [{maladaptive_schema}]의 원인)"
                response = search_agent.invoke(search_instruction, cfg, chat_history=st.session_state.messages2)
                output = json.loads(response["output"])["action_input"] if "{" in response["output"]  else response["output"]
                st.write(f'{output}')
                st.session_state.messages2.append(
                        {
                            "role": "assistant",
                            "content": output
                        })
