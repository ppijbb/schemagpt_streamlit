import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import torch
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.retrievers import MultiQueryRetriever
from langchain.retrievers.multi_query import LineListOutputParser
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
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
            metadata = {
                "_id": uuid.uuid4().hex
            }
            if metadata:
                metadata.update(metadata)
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=uuid.uuid4().hex ,
                        vector=vector,
                        payload={
                            # "text": text,
                            "page_content": text,
                            "metadata": metadata
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
                    "text": result.payload["text"],
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
    # Base retriever
    base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    # Multi-query retriever
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=get_llm(),
        parser_key="lines"
    )

    # Compression/Reranking retriever
    compressor = LLMChainExtractor.from_llm(get_llm())
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    # Ensemble retriever
    ensemble_retriever = EnsembleRetriever(
        retrievers=[multi_query_retriever, compression_retriever],
        weights=[0.5, 0.5]
    )
    
    return ensemble_retriever

# Initialize RAG chain
def get_rag_chain(vectorstore: VectorStore):
    retriever = get_adaptive_retriever(vectorstore.vectorstore)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """제공된 Context를 기반으로 질문에 답변해주세요.
        만약 Context에 관련 정보가 없다면 '처리할 수 없는 질문입니다.'라고 답변해주세요.
        전문적이고 도움이 되는 톤으로 답변해주세요."""),
        ("user", "Context: {context}\n\n질문: {question}")
    ])
    chain = (
        RunnableParallel({
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question")
        })
        | {
            "context": lambda x: "\n".join([doc.page_content for doc in x["context"]]),
            "question": itemgetter("question")
        }
        | prompt
        | get_llm()
        | StrOutputParser()
    )
    return chain