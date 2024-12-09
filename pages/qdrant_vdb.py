import streamlit as st
import numpy as np
import uuid
import traceback

from srcs.qdrant_vdb import get_rag_chain
from srcs.st_cache import init_vectorstore, get_or_create_eventloop

# LangGraph 시각화를 위한 import 추가
import json
from pyvis.network import Network
import streamlit.components.v1 as components
from srcs.st_utils import draw_mermaid
import streamlit_mermaid as stmd

get_or_create_eventloop()


st.set_page_config(
    page_title="Qdrant Vector DB",
    page_icon="🔍",
    layout="wide"
)

st.title('🔍 Qdrant Vector Database')

st.markdown('''
## 프로젝트 소개

    Qdrant Vector Database 테스트 페이지
    벡터 데이터베이스의 기본적인 CRUD 작업 테스트

## 개발 내용
- 벡터 데이터 생성 및 저장
- 벡터 검색
- 컬렉션 관리

## 사용 기술
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
''', unsafe_allow_html=True)

vector_store = init_vectorstore()
chain = get_rag_chain(vector_store)

insert_section, info_section = st.columns(2)
with insert_section:
    # 데이터 입력 섹션
    st.header("텍스트 데이터 입력")
    text_input = st.text_area(
        label="텍스트 입력",
        height=100,
        help="저장하고 싶은 텍스트를 입력하세요. 이 텍스트는 벡터로 변환되어 저장됩니다.")
    metadata = st.text_input(
        label="메타데이터 (선택사항)",
        help="텍스트에 대한 추가 정보를 입력하세요 (예: 제목, 카테고리 등)")

if st.button("텍스트 추가"):
    # 텍스트를 벡터로 변환
    if vector_store.add_text(text_input.strip(), metadata):
        st.success("텍스트가 성공적으로 추가되었습니다!")
    else:
        st.error("텍스트를 입력해주세요!")
search_section, result_section = st.columns(2)
with search_section:
    # 검색 섹션
    st.header("텍스트 검색")
    search_text = st.text_input(
        label="검색할 텍스트를 입력하세요",
        help="찾고자 하는 텍스트와 의미적으로 유사한 데이터를 검색합니다.")
with result_section:
    st.subheader("검색 결과")

if st.button("검색"):
    if search_text.strip():
        # 검색 텍스트를 벡터로 변환
        search_results = vector_store.search(search_text)
        if search_results:
            for result in search_results:
                with result_section:
                    with st.expander(f"유사도: {result['score']:.4f}"):
                        st.write("📝 텍스트:")
                        st.write(result["text"])
                        st.write("ℹ️ 메타데이터:")
                        st.write(result["metadata"])
        else:
            result_section.info("검색 결과가 없습니다.")
    else:
        result_section.error("검색할 텍스트를 입력해주세요!")
        
with info_section:
    # 컬렉션 정보 표시
    st.header("컬렉션 정보")
    collection_info = vector_store.get_collection_info()
    del collection_info["config"]
    st.json(collection_info)

# 컬렉션 정보 표시 섹션 아래에 다음 코드를 추가
st.header("💬 RAG 채팅 테스트")
st.markdown("""
이 섹션에서는 Qdrant 벡터 데이터베이스를 활용한 RAG(Retrieval-Augmented Generation) 채팅을 테스트할 수 있습니다.
""")

# 사이드바에 OpenAI API 키 입력
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", type="password")
#     if not openai_api_key:
#         st.warning("Please enter your OpenAI API key to test the chat functionality.")

# 채팅 인터페이스
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_section, graph_section = st.columns([0.7, 0.3])

with chat_section:
    # 이전 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("질문을 입력하세요"):

        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 어시스턴트 응답 생성
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                # RAG 체인 실행
                response = chain.invoke({"question": prompt})
                # 응답 표시
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                print(traceback.format_exc())
                st.error(f"Error generating response: {str(e)}")

    # 채팅 초기화 버튼
    if st.button("채팅 초기화"):
        st.session_state.messages = []
        st.experimental_rerun()

with graph_section:
    # LangGraph 시각화
    if hasattr(chain, 'get_graph'):  # LangGraph 결과가 있는 경우
        st.subheader("🔍 검색 및 추론 과정")
        # 노드와 엣지 추가
        graph_data = chain.get_graph()
        # st.image(graph_data.draw_mermaid_png())
        stmd.st_mermaid(graph_data.draw_mermaid(), width="100%", height="800px")
        # draw_mermaid(graph_data.draw_mermaid())
        # 상세 정보 표시
        if hasattr(graph_data, 'process_details'):
            with st.expander("📊 상세 처리 과정"):
                for step in graph_data.process_details:
                    st.markdown(f"**{step['step']}**")
                    st.markdown(step['description'])
                    if 'data' in step:
                        st.json(step['data'])
                    
