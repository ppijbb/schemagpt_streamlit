__import__('pysqlite3')
import os
import asyncio
import sys
import copy
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import pandas as pd
import streamlit as st

from langchain.callbacks.manager import CallbackManager
from langchain_core.runnables import RunnableConfig
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.agents import initialize_agent, AgentType, ConversationalChatAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from langchain_openai import ChatOpenAI
from srcs import schema_therapy


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_utterance_data(url="/"):
    try:
        embedding_function = SentenceTransformerEmbeddings(model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS")
    except Exception as e:
        print(e)
        embedding_function = OpenAIEmbeddings()
    data = DataFrameLoader(pd.read_excel("schema_utterance.xlsx"), page_content_column="domain").load()

    return Chroma.from_documents(
        #  collection_name="schema_collection",
        persist_directory="./chromadb_oai",
        documents=data,
        embedding=embedding_function, )


os.environ["TOKENIZERS_PARALLELISM"] = "0"

if "shared" not in st.session_state:
   st.session_state["shared"] = True

vector_db = get_utterance_data()

st.title('🦜🔗 Quickstart App')
with st.sidebar:
    st.page_link("pages/cardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)

    try:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
    except Exception as e:
            openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

col1, col2 = st.columns(2)

with col1:
    st.title("🔎 Chat with DuckDuckgo")
    """
    In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
    Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
    """
    col1_chat_container = st.container()
    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferMemory(
        chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": "당신은 한국어 전문가 GPT입니다."
            },
            {
                "role": "assistant",
                "content": "Hi, I'm a chatbot who can search the web. How can I help you?"
            }]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            col1_chat_container.chat_message(msg["role"]).write(msg["content"])

    if col1_prompt := col1.chat_input(placeholder="Who won the Women's U.S. Open in 2018?", key=col1):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": col1_prompt
            })
        col1_chat_container.chat_message("user").write(col1_prompt)
        searched_result = vector_db.similarity_search(col1_prompt)[0]

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        final_streaming_cb = FinalStreamingStdOutCallbackHandler()

        llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                         openai_api_key=openai_api_key,
                         streaming=True,
                         callback_manager=CallbackManager([final_streaming_cb]))
        search = DuckDuckGoSearchRun(region="kr-kr", time="n")
        search_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=[search])
        executor = AgentExecutor.from_agent_and_tools(
            agent=search_agent,
            tools=[search],
            memory=memory,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
        )
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        response = executor.invoke(st.session_state.messages, cfg,)
        col1_chat_container.chat_message("assistant").write(f'{response["output"]}')
        st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response["output"]
                })


with col2:
    st.title("🔎 Something else...")

    """
    In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
    Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
    """
    col2_chat_container = st.container()
    if "messages2" not in st.session_state:
        st.session_state["messages2"] = [
            {
                "role": "system",
                "content": """
SYSTEM:
당신은 정신 건강 상담사입니다.
먼저 당신은 대화 단계를 파악하고 그 단계에 맞는 대답을 제공해야합니다.
다음, 당신은 괄호 안에 있는 사용자 지시사항을 명심해야합니다.
그리고 친절한 말투로 사용자에게 응원, 공감, 안정, 조언을 해주세요.
마지막으로 절대 괄호 안에 있는 사용자 지시사항을 직접적으로 말하지 마세요.
 
대화 단계는 종료와 진행이 있습니다.
- 종료: 대화가 충분히 진행 된 이후 사용자가 대화를 마무리하고 싶어할 때 단계
- 진행: 종료 이외의 모든 단계
 
[INST]
위에 주어진 가이드라인을 따라서,
먼저 사용자 메세지로부터 대화의 단계를 구분합니다.
사용자 메세지에 어떻게 답변을 할지 생각합니다.
그리고 괄호 안의 지시사항을 따라 사용자의 감정 표현을 이끌어낼 수 있는 답변을 생성해주세요.
답변은 답변: 뒤에 작성합니다.
한국어로만 답변합니다.
 
<example>
user: 요즘에는 별다른 일이 없어서 그런지 뭔가 지루하다는 느낌이 들어요.(사용자가 적극적으로 표현할 수 있도록 대화를 진행해주세요)
you: 단계: 진행
답변: 지루하지만 한편으로는 평안하지 않으세요? 전 별다른 일이 없다는 게 한편으로는 좋아보여요!
</example>
"""
            },
            {
                "role": "assistant",
                "content": "안녕하세요? 무엇을 도와드릴까요?"
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
        search = DuckDuckGoSearchRun(name="Search",
                                     time="d",
                                     max_results=3)
        search_agent = initialize_agent(tools=[search],
                                        llm=llm,
                                        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                        handle_parsing_errors=True)
        cfg = RunnableConfig()
        cfg["callbacks"] = [StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)]
        search_instruction = copy.deepcopy(st.session_state.messages2)
        search_instruction[-1]["content"] += f"\n(해당문장에서 비롯된 심리 도식 [{maladaptive_schema}]의 원인)"
        response = search_agent.invoke(search_instruction, cfg,)
        col2_chat_container.chat_message("assistant").write(f'{response["output"]}')
        st.session_state.messages2.append(
                {
                    "role": "assistant",
                    "content": response["output"]
                })
