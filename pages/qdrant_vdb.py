"""
Advanced RAG 챗봇 서비스 (Qdrant Vector DB).
Streamlit Cloud 호환: in-memory Qdrant, CPU 임베딩, st.secrets API 키.
"""
import asyncio
import os

import streamlit as st
from langchain_core.messages import HumanMessage

from srcs.qdrant_vdb import VectorStore, get_rag_chain
from srcs.st_cache import init_vectorstore

# Streamlit Cloud: 이벤트 루프 설정
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Advanced RAG (Qdrant)",
        page_icon="🔗",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title("🔗 Advanced RAG 챗봇 서비스")
    st.caption("Qdrant in-memory + Multi-Query + BM25 Ensemble + Contextual Compression")

    # Streamlit Cloud: API 키는 secrets 또는 환경변수 사용 (하드코딩 금지)
    with st.sidebar:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            api_key = st.text_input(
                "OpenAI API Key (DDG 챗 사용 시 필요)",
                key="qdrant_openai_key",
                type="password",
            )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

    # VectorStore는 메모리 내부 (:memory:) — Cloud 재시작 시 초기화됨
    try:
        vectorstore: VectorStore = init_vectorstore()
    except Exception as e:
        st.error(f"VectorStore 초기화 실패: {e}")
        st.stop()

    tab_add, tab_search, tab_rag = st.tabs(["📄 문서 추가", "🔍 유사도 검색", "💬 RAG 챗봇"])

    with tab_add:
        st.subheader("문서 추가")
        doc_text = st.text_area("저장할 텍스트", height=120, key="qdrant_add_text")
        if st.button("저장", key="qdrant_add_btn"):
            if doc_text and doc_text.strip():
                if vectorstore.add_text(doc_text.strip()):
                    st.success("저장되었습니다.")
                else:
                    st.error("저장에 실패했습니다.")
            else:
                st.warning("텍스트를 입력하세요.")

    with tab_search:
        st.subheader("유사도 검색")
        query = st.text_input("검색 쿼리", key="qdrant_search_query")
        limit = st.slider("결과 수", 1, 20, 5, key="qdrant_search_limit")
        if st.button("검색", key="qdrant_search_btn") and query:
            results = vectorstore.search(query, limit=limit)
            if results:
                for i, r in enumerate(results, 1):
                    with st.expander(f"#{i} (score: {r.get('score', 0):.4f})"):
                        st.write(r.get("text", ""))
                        if r.get("metadata"):
                            st.caption(str(r["metadata"]))
            else:
                st.info("결과가 없습니다.")

    with tab_rag:
        st.subheader("RAG 챗봇")
        system_prompt = st.text_area(
            "시스템 프롬프트",
            value="당신은 주어진 Context를 바탕으로만 답변하는 어시스턴트입니다. Context에 없는 내용은 추측하지 마세요.",
            height=80,
            key="qdrant_rag_system",
        )

        if "qdrant_rag_memory" not in st.session_state:
            from langchain.memory import ConversationBufferMemory
            st.session_state["qdrant_rag_memory"] = ConversationBufferMemory(
                return_messages=True,
                memory_key="history",
            )

        memory = st.session_state["qdrant_rag_memory"]
        if st.sidebar.button("대화 초기화", key="qdrant_rag_clear"):
            memory.clear()
            st.session_state.pop("qdrant_rag_memory", None)
            from langchain.memory import ConversationBufferMemory
            st.session_state["qdrant_rag_memory"] = ConversationBufferMemory(
                return_messages=True,
                memory_key="history",
            )
            st.rerun()

        chat_container = st.container()
        with chat_container:
            history = memory.load_memory_variables({}).get("history", [])
            for msg in history:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                with st.chat_message(role):
                    st.write(msg.content if hasattr(msg, "content") else str(msg))

        if prompt := st.chat_input("RAG 질문 입력"):
            with st.chat_message("user"):
                st.write(prompt)
            try:
                chain = get_rag_chain(vectorstore, system_prompt.strip(), memory)
                response = chain.invoke({"question": prompt})
                memory.save_context({"input": prompt}, {"output": response})
                with st.chat_message("assistant"):
                    st.write(response)
                st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")
