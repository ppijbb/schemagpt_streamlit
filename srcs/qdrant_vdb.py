import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import torch
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import LineListOutputParser
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import MultiQueryRetriever, EnsembleRetriever, ContextualCompressionRetriever, BM25Retriever
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda, RunnableSerializable

from langchain.schema import StrOutputParser
from operator import itemgetter
from typing import List, Tuple, Dict, Optional, Any

from srcs.langchain_llm import DDG_LLM
from srcs.st_cache import get_llm

        
class VectorStore:
    def __init__(self, collection_name: str = "test_collection"):
        self.collection_name = collection_name
        self.client = self._init_client()
        self.embeddings = self._get_embeddings()
        self.embedding_dimensions = self._get_embedding_dimensions()
        self.vectorstore = self._init_vectorstore()
        self._ensure_collection()       

    def _init_vectorstore(self):
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
            
        )

    def _init_client(self):
        return QdrantClient(":memory:")  # 메모리에서 실행 (테스트용)

    def _get_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
        )

    def _get_embedding_dimensions(self):
        return self.embeddings.client.get_sentence_embedding_dimension()

    def _ensure_collection(self):
        """컬렉션이 없으면 생성"""
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.embedding_dimensions,  # 임베딩 차원
                    distance=models.Distance.COSINE
                )
            )

    def add_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """텍스트를 벡터로 변환하여 저장"""
        if not text.strip():
            return False

        try:
            vector = self.embeddings.embed_query(text)
            _metadata = {
                "_id": uuid.uuid4().hex
            }
            if metadata:
                _metadata.update(metadata)
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=uuid.uuid4().hex ,
                        vector=vector,
                        payload={
                            # "text": text,
                            "page_content": text,
                            "metadata": _metadata
                        }
                    )
                ]
            )
            return True
        except Exception as e:
            st.error(f"Error adding text: {e}")
            return False

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """텍스트로 유사한 문서 검색"""
        try:
            search_vector = self.embeddings.embed_query(query)
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=search_vector,
                limit=limit
            )
            return [
                {
                    "text": result.payload["page_content"],
                    "metadata": result.payload["metadata"],
                    "score": result.score
                }
                for result in results
            ]
        except Exception as e:
            st.error(f"Error searching: {e}")
            return []

    def get_collection_info(self) -> Dict:
        """컬렉션 정보 조회"""
        try:
            info = self.client.get_collection(self.collection_name)
            return info.model_dump()
        except Exception as e:
            st.error(f"Error getting collection info: {e}")
            return {}

    def delete_collection(self) -> bool:
        """컬렉션 삭제"""
        try:
            self.client.delete_collection(self.collection_name)
            return True
        except Exception as e:
            st.error(f"Error deleting collection: {e}")
            return False

    def as_retriever(self, k: int = 5):
        """LangChain 리트리버 반환"""
        return self.vectorstore.as_retriever(search_kwargs={"k": k})


# Adaptive RAG components
def generate_queries(question: str) -> List[str]:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
            # Start of Selection
            ("system", "제공된 질문에 대해 관련 컨텍스트를 검색하기 위해 3가지 다른 버전의 질문을 생성하세요. 다양하게 만드세요."),
            ("user", "{question}")
    ])
    chain = prompt | llm | LineListOutputParser()
    return chain.invoke({"question": question})

def get_adaptive_retriever(vectorstore):
    # Base vector retriever
    vector_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    # Multi-query retriever
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=vector_retriever,
        llm=get_llm(),
        parser_key="lines"
    )

    # BM25 retriever 초기화
    # vectorstore에서 모든 문서 가져오기
    all_docs = []
    try:
        results = vectorstore.client.scroll(
            collection_name=vectorstore.collection_name,
            limit=1000  # 적절한 수로 조정
        )[0]
        for result in results:
            if result.payload.get("page_content"):  # 유효한 문서만 추가
                all_docs.append(
                    Document(
                        page_content=result.payload.get("page_content", ""),
                        metadata=result.payload.get("metadata", {})
                    )
                )
    except Exception as e:
        st.warning(f"BM25 초기화 중 오류 발생: {e}")
        all_docs = []

    # 문서가 있을 때만 BM25와 Ensemble 사용
    if all_docs:
        # BM25 retriever 설정
        bm25_retriever = BM25Retriever.from_documents(all_docs)
        bm25_retriever.k = 5  # 검색 결과 수 설정

        # Ensemble retriever (Vector + BM25)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[multi_query_retriever, bm25_retriever],
            weights=[0.7, 0.3]  # 벡터 검색에 더 높은 가중치
        )
        base_retriever = ensemble_retriever
    else:
        # 문서가 없으면 multi-query retriever만 사용
        st.info("데이터베이스가 비어있어 벡터 검색만 수행합니다.")
        base_retriever = multi_query_retriever

    # Compression/Reranking retriever 적용
    compressor = LLMChainExtractor.from_llm(get_llm())
    final_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )
    
    return final_retriever

# Initialize RAG chain
def get_rag_chain(
    vectorstore: VectorStore, 
    system_prompt: str, 
    memory: ConversationBufferMemory
    )-> RunnableSerializable:

    def _process_context(step_output):
        result = []
        for doc in step_output['context']:
            source_data = doc.page_content.strip()
            metadata_text = "\n".join([f"{k}:{v}" for k, v in doc.metadata.items()])
            result.append(f"{source_data}\n{metadata_text}")
        return "\n".join(result)
    
    retriever = get_adaptive_retriever(vectorstore.vectorstore)
    
    # Start of Selection
    chain = (
        RunnableParallel({
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "history": RunnablePassthrough.assign(
                history=RunnableLambda(memory.load_memory_variables)
                        | itemgetter(memory.memory_key)
                ) 
                | itemgetter("history")
        })
        | {
            "context": _process_context,
            "question": itemgetter("question"),
            "history": RunnablePassthrough.assign(
                history=RunnableLambda(memory.load_memory_variables)
                        | itemgetter(memory.memory_key)
                )
                | itemgetter("history")
        }
        | ChatPromptTemplate.from_messages([
                SystemMessage(content=system_prompt),
                MessagesPlaceholder("history"),
                HumanMessage(content="{question}\n\nContext:\n{context}"),
            ])
        | get_llm()
        | StrOutputParser()
    )
    return chain
