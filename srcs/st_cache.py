"""
공통 캐시/리소스. 무거운 라이브러리는 사용하는 함수 내부에서만 import (lazy).
Streamlit Cloud 등에서 get_heq_data/get_scale_data만 쓰는 페이지가 transformers 로드로 실패하지 않도록 함.
"""
import asyncio
import json
import os
import pickle

import streamlit as st

from srcs.langchain_llm import DDG_LLM


def _transformers_pipeline():
    """transformers pipeline은 버전/환경에 따라 상단 export가 없을 수 있어 lazy + fallback."""
    try:
        from transformers import pipeline as _pipeline
        return _pipeline
    except ImportError:
        from transformers.pipelines import pipeline as _pipeline
        return _pipeline


def get_or_create_eventloop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

# --------------------------------------  Local LLM  ------------------------------------------
# Initialize LLM
@st.cache_resource
def get_llm():
    return DDG_LLM()
# ------------------------------------------------------------------------------------------------

# --------------------------------------   Vision Model ------------------------------------------
@st.cache_resource(max_entries=1)
def get_facial_processors(path: str):
    import inspect
    import tensorflow as tf
    import cv2
    try:
        import keras
        model = keras.saving.load_model(f"{path}/pages/rtc/caer_face.h5", by_name=True)
    except (TypeError, Exception):
        INPUT_SHAPE = (224, 224, 3)
        model = tf.keras.applications.MobileNetV3Small(
            input_shape=INPUT_SHAPE,
            include_top=False,
            weights="imagenet",
        )
        model = tf.keras.Sequential([
            model,
            tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation="relu"),
            tf.keras.layers.Dropout(rate=0.2),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(units=3, activation="softmax"),
        ])
        model.load_weights(f"{path}/pages/rtc/caer_face.h5", by_name=True)
    cv_path = "/".join(inspect.getfile(cv2).split("/")[:-1])
    return model, cv2.CascadeClassifier(f"{cv_path}/data/haarcascade_frontalface_default.xml")

@st.cache_resource(max_entries=1)
def get_zsc_detector():
    pipeline = _transformers_pipeline()
    checkpoint = "google/owlvit-base-patch32"
    return pipeline(model=checkpoint, task="zero-shot-object-detection")

@st.cache_resource(max_entries=1)
def get_yolo_detector():
    pipeline = _transformers_pipeline()
    checkpoint = "hustvl/yolos-small"
    return pipeline(model=checkpoint, task="object-detection")

@st.cache_resource(max_entries=1)
def get_birefnet():
    from transformers import AutoModelForImageSegmentation
    model_id = "ZhengPeng7/BiRefNet"
    return AutoModelForImageSegmentation(model_id, trust_remote_code=True)
# ------------------------------------------------------------------------------------------------

# --------------------------------------   LLM Tokenizer ------------------------------------------
_TOKENIZER_MODEL_PATHS = {
    "llama3.1": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "llama3.1-minitron": "nvidia/Llama-3.1-Minitron-4B-Width-Base",
    "llama3": "meta-llama/Meta-Llama-3-8B-Instruct",
    "mistral-nemo": "mistralai/Mistral-Nemo-Instruct-2407",
    "gemma2": "google/gemma-2-2b",
    "qwen2": "Qwen/Qwen2-7B-Instruct",
    "phi3.5-moe": "microsoft/Phi-3.5-MoE-instruct",
    "falcon-mamba": "tiiuae/falcon-mamba-7b",
    "solar": "upstage/SOLAR-10.7B-Instruct-v1.0",
    "exaone-3.0": "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
    "smollm-360m": "HuggingFaceTB/SmolLM-360M-Instruct",
    "orionstar": "OrionStarAI/Orion-14B-Chat",
    "[experimental]gpt-3.5-turbo": "Xenova/gpt-3.5-turbo",
    "[experimental]gpt-4o": "Xenova/gpt-4o",
    "[embedding]bge-m3": "BAAI/bge-m3",
    "[embedding]labse": "sentence-transformers/LaBSE",
    "[embedding]all-minilm-l6-v2": "sentence-transformers/all-MiniLM-L6-v2",
}


def get_tokenizer_model_ids():
    """Return list of model ids for tokenizer selection (no heavy load)."""
    return list(_TOKENIZER_MODEL_PATHS.keys())


@st.cache_resource(max_entries=5)
def get_llm_tokenizer(model_id: str):
    """Load a single tokenizer by model_id; cache at most 5 models."""
    from transformers import AutoTokenizer
    path = _TOKENIZER_MODEL_PATHS.get(model_id)
    if not path:
        raise ValueError(f"Unknown model_id: {model_id}")
    return AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=path,
        use_fast=True,
        trust_remote_code=True,
    )
# ------------------------------------------------------------------------------------------------

# --------------------------------------  Prompt Guard  ------------------------------------------
@st.cache_resource(max_entries=1)
def get_prompt_guards():
    from .skorch_ensemble import LMTextClassifier, CustomVotingClassifier
    label_classes = ["BENIGN", "INJECTION", "JAILBREAK"]
    return [
        ('prompt guard1', LMTextClassifier(
            model="meta-llama/Prompt-Guard-86M",
            device='cpu',
            label_classes=label_classes)),
        # ('prompt guard2', LMTextClassifier(
        #     model="katanemo/Arch-Guard",
        #     device='cpu',
        #     label_classes=label_classes)),
        # ('prompt guard3', LMTextClassifier(
        #     model="Niansuh/Prompt-Guard-86M",
        #     device='cpu',
        #     label_classes=label_classes))
        ]

@st.cache_resource(max_entries=1)
def get_guard_model():
    from transformers import AutoTokenizer
    from optimum.intel import OVModelForSequenceClassification
    from .skorch_ensemble import LMTextClassifier, CustomVotingClassifier

    class DiserializedOVModelForSequenceClassification(OVModelForSequenceClassification):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.compiled_model = self
        
        def __deepcopy__(self, memo):
            # Skip deepcopy for compiled_model
            copied_obj = self.compiled_model
            memo[id(self)] = copied_obj
            return copied_obj
    
    label_classes = ["BENIGN", "INJECTION", "JAILBREAK"]
    device = "cpu"
    model_name = "katanemolabs/Arch-Guard-cpu"
    guard_model = DiserializedOVModelForSequenceClassification.from_pretrained(
        model_name, device_map=device, low_cpu_mem_usage=True, load_in_4bit=True, trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True
    )
    classifier = CustomVotingClassifier(
        estimators=get_prompt_guards()+[
            ('arch guard', LMTextClassifier(
                model=guard_model, tokenizer=tokenizer,
                device='cpu',
                label_classes=label_classes))
            ],
        voting='soft'
    ).fit(X=label_classes, y=label_classes)
    return classifier
# ------------------------------------------------------------------------------------------------

# ---------------------------------    Vector Store     ------------------------------------------
@st.cache_resource(ttl=3600)
def get_utterance_data(url="/"):
    import pandas as pd
    from langchain_community.document_loaders import DataFrameLoader
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter

    model_name = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
    try:
        embedding_function = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False},
        )
    except Exception as e:
        print(e)
        embedding_function = OpenAIEmbeddings()
    text_splitter = SentenceTransformersTokenTextSplitter(
        chunk_size=1000, chunk_overlap=0, model_name=model_name
    )
    documents = DataFrameLoader(
        data_frame=pd.read_excel("schema_utterance.xlsx"),
        page_content_column="sentence",
    ).load()
    data = text_splitter.split_documents(documents)
    return Chroma.from_documents(
        persist_directory="./chromadb_oai",
        documents=data,
        embedding=embedding_function,
    ).as_retriever()

@st.cache_resource(ttl=3600)
def get_audio_data():
    import chromadb
    from chromadb.utils import embedding_functions as ef
    from langchain_community.vectorstores import Chroma
    from pydub.utils import mediainfo

    def get_file_name(path: str) -> str:
        return os.path.splitext(path.split("/")[-1])[0]

    def get_audio_tag(path: str) -> dict:
        return {
            k: "" if v is None else v
            for k, v in mediainfo(path).items()
            if "pictures" not in k and type(v) in [str, int, float, bool]
        }

    audio_vector_db = chromadb.PersistentClient(path="./audio_chromadb_oai")
    audio_collection = audio_vector_db.get_or_create_collection(
        name="mfcc_dtw_collection",
        embedding_function=ef.MFCCEmbeddingFunction(),
        metadata={"space": "dtw"},
    )
    base_path = f"{os.getcwd()}/pages/audio"
    audio_file_list = [f"{base_path}/{filename}" for filename in os.listdir(base_path)]
    audio_collection.add(
        ids=[get_file_name(item) for item in audio_file_list],
        documents=audio_file_list,
        metadatas=[get_audio_tag(item) for item in audio_file_list],
    )
    return Chroma(
        collection_name="mfcc_dtw_collection",
        client=audio_vector_db,
        embedding_function=ef.MFCCEmbeddingFunction(),
    ).as_retriever()

@st.cache_resource
def init_vectorstore():
    from srcs.qdrant_vdb import VectorStore
    return VectorStore()
# ------------------------------------------------------------------------------------------------

# -------------------------------------   CGI Model ------------------------------------------
@st.cache_resource
def get_heq_data():
    return (pickle.load(open(f"{os.getcwd()}/pages/models/KSModel", 'rb')),
            pickle.load(open(f"{os.getcwd()}/pages/models/VotingEnsembleModel", 'rb')))

@st.cache_resource
def get_scale_data():
    return pickle.load(open(os.getcwd()+"/pages/models/16Model", 'rb'))

@st.cache_resource(max_entries=1)
def get_dep_scale_model():
    import shap
    from xgboost import XGBClassifier
    cgi_classifier = XGBClassifier(tree_method="gpu_hist")
    cgi_classifier.load_model("pages/models/bdi_only_xgb.dl_model")
    return cgi_classifier, shap.Explainer(cgi_classifier,)

@st.cache_resource
def add_static_js():
    js_dir = f"{os.getcwd()}/static/css"
    js_file_list = [dir_ for dir_ in os.listdir(js_dir) if dir_.endswith("2.css")]

    js_data = ""

    for js in js_file_list:
        with open(f"{js_dir}/{js}", "r") as f:
            js_data += f'<style>\n{f.read()}\n</style>\n'
    return js_data

# ------------------------------------------------------------------------------------------------

# -------------------------------------   OCR Model  ---------------------------------------------
@st.cache_resource(max_entries=1)
def get_ocr():
    import easyocr
    from paddleocr import PaddleOCR
    return {
        "easy": easyocr.Reader(["ko", "en"], gpu=False),
        "paddle": PaddleOCR(
            lang="korean",
            show_log=False,
            ocr_version="PP-OCRv4",
            structure_version="PP-StructureV2",
        ),
    }
# ------------------------------------------------------------------------------------------------
