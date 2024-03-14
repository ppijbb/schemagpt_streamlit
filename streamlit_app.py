__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import pandas as pd
import streamlit as st
import os
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.retrievers.web_research import WebResearchRetriever
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings


os.environ["TOKENIZERS_PARALLELISM"]="0"

if "shared" not in st.session_state:
   st.session_state["shared"] = True

try:
    embedding_function = SentenceTransformerEmbeddings(model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS")
except Exception as e:
    print(e)
    embedding_function = OpenAIEmbeddings()
data = DataFrameLoader(pd.read_excel("schema_utterance.xlsx"), page_content_column="domain").load()

vector_db = Chroma.from_documents(
    collection_name="schema_collection",
    persist_directory="./chromadb_oai",
    documents=data,
    embedding=embedding_function,)

st.title('🦜🔗 Quickstart App')
with st.sidebar:
    st.page_link("pages/cardio.py", label="Demo1")
    st.page_link("pages/dep_peptide.py", label="Demo2")
    st.page_link("pages/facial.py", label="Demo3")

    try:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
    except Exception as e:
            openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
col1, col2 = st.columns(2)

with col1:
    st.title("🔎 LangChain - Chat with search")

    """
    In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
    Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
    """

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Hi, I'm a chatbot who can search the web. How can I help you?"
            }]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?", key=col1):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            })
        st.chat_message("user").write(prompt)
        searched_result = vector_db.similarity_search(prompt)[0]

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
        # search = DuckDuckGoSearchRun(name="Search")
        # search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            # response = search_agent.invoke(st.session_state.messages, callbacks=[st_cb])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f'{searched_result}'
                })
            st.write(response)


with col2:
    st.title("🔎 LangChain - Chat with search")

    """
    In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
    Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
    """
