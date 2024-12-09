import os
import pickle
import asyncio
import json

import streamlit as st
import torch
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import keras
import inspect
import cv2
import pandas as pd
from xgboost import XGBClassifier
from transformers import pipeline, AutoTokenizer, AutoModelForImageSegmentation
import shap
import easyocr
import paddle
from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter
from langchain_community.vectorstores import Chroma, Qdrant

import chromadb
from chromadb.utils import embedding_functions as ef
from qdrant_client import QdrantClient
from qdrant_client.http import models


from srcs.langchain_llm import DDG_LLM


import pydub
from pydub.utils import mediainfo


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

# --------------------------------------  Local LLM  ------------------------------------------
# Initialize LLM
@st.cache_resource
def get_llm():
    return DDG_LLM()
# ------------------------------------------------------------------------------------------------

# --------------------------------------   Vision Model ------------------------------------------
@st.cache_resource
def get_facial_processors(path: str):
    # load model
    try:
        with open(f"{path}/pages/rtc/caer_face.json" , "r") as j:
            # model = model_from_json(j.read())
            # load weights
            keras.saving.load_model(f"{path}/pages/rtc/caer_face.h5", by_name=True)

    except TypeError:
        INPUT_SHAPE = (224, 224, 3)
        model = tf.keras.applications.MobileNetV3Small(input_shape=INPUT_SHAPE,
                                                       include_top=False,
                                                       weights="imagenet")
        model = tf.keras.Sequential([
            model,
            tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation="relu"),
            tf.keras.layers.Dropout(rate=0.2),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(units=3, activation="softmax")
        ])
        model.load_weights(f"{path}/pages/rtc/caer_face.h5", by_name=True)

        # model = load_model(f"{path}/pages/rtc/caer_face.h5")

    # mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solutions.drawing_styles
    # mp_hands = mp.solutions.hands
    # hands = mp_hands.Hands(
    #     model_complexity=0,
    #     min_detection_confidence=0.5,
    #     min_tracking_confidence=0.5
    # )

    # face detection
    cv_path = "/".join(inspect.getfile(cv2).split("/")[:-1])
    return model, cv2.CascadeClassifier(f"{cv_path}/data/haarcascade_frontalface_default.xml")

@st.cache_resource
def get_zsc_detector():
    # "Thomasboosinger/owlv2-base-patch16-ensemble"  #
    checkpoint = "google/owlvit-base-patch32"
    return pipeline(model=checkpoint, task="zero-shot-object-detection")

@st.cache_resource
def get_yolo_detector():
    # "devonho/detr-resnet-50_finetuned_cppe5"
    checkpoint = "hustvl/yolos-small"
    return pipeline(model=checkpoint, task="object-detection")

@st.cache_resource
def get_birefnet():
    model_id = "ZhengPeng7/BiRefNet"
    return AutoModelForImageSegmentation(model_id, trust_remote_code=True)
# ------------------------------------------------------------------------------------------------

# --------------------------------------   LLM Tokenizer ------------------------------------------
@st.cache_resource
def get_llm_tokenizer():
    # "devonho/detr-resnet-50_finetuned_cppe5"
    tokenizer_list = {
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
        # "[experimental]openai-embedding-ada": "Xenova/text-embedding-ada-002",
        "[embedding]bge-m3": "BAAI/bge-m3",
        "[embedding]labse": "sentence-transformers/LaBSE",
        "[embedding]all-minilm-l6-v2": "sentence-transformers/all-MiniLM-L6-v2",
    }
    return { 
        k: AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=v, 
            use_fast=True, 
            trust_remote_code=True) 
        for k, v in tokenizer_list.items() 
    }
# ------------------------------------------------------------------------------------------------

# --------------------------------------  Prompt Guard  ------------------------------------------
@st.cache_resource
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

@st.cache_resource
def get_guard_model():
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
@st.cache_resource
def get_utterance_data(url="/"):
    model_name = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
    try:
        # embedding_function = SentenceTransformerEmbeddings(model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS")
        embedding_function = HuggingFaceEmbeddings(model_name=model_name,
                                                   model_kwargs={'device': 'cpu'},
                                                   encode_kwargs={'normalize_embeddings': False})
    except Exception as e:
        print(e)
        embedding_function = OpenAIEmbeddings()
    
    text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=1000, 
                                                          chunk_overlap=0, 
                                                          model_name=model_name)
    documents = DataFrameLoader(data_frame=pd.read_excel("schema_utterance.xlsx"), 
                                page_content_column="sentence").load()
    data = text_splitter.split_documents(documents)
    return Chroma.from_documents(# collection_name="schema_collection",
                                 persist_directory="./chromadb_oai",
                                 documents=data,
                                 embedding=embedding_function, ).as_retriever()

@st.cache_resource
def get_audio_data():

    def get_file_name(path:str)->str:
        return os.path.splitext(path.split("/")[-1])[0]

    def get_audio_tag(path:str)->dict:
        return {
            k: "" if v is None else v
            for k, v in mediainfo(path).items()
            if "pictures" not in k
            and type(v) in [str, int, float, bool]
        }

    audio_vector_db = chromadb.PersistentClient(path="./audio_chromadb_oai")
    audio_collection = audio_vector_db.get_or_create_collection(
        name="mfcc_dtw_collection",
        embedding_function=ef.MFCCEmbeddingFunction(), # Custom Audio Embedding function
        metadata={ "space": "dtw" }
    )
    base_path = f"{os.getcwd()}/pages/audio"
    audio_file_list = [f"{base_path}/{filename}" for filename in os.listdir(base_path)]
    audio_collection.add(
        ids=[get_file_name(item) for item in audio_file_list],
        documents=audio_file_list,
        metadatas=[get_audio_tag(item) for item in audio_file_list]
    )

    return Chroma(
        collection_name="mfcc_dtw_collection",
        client=audio_vector_db,
        embedding_function=ef.MFCCEmbeddingFunction() # Custom Audio Embedding function
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

@st.cache_resource
def get_dep_scale_model():
    cgi_classifier = XGBClassifier(tree_method='gpu_hist')
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
@st.cache_resource
def get_ocr():
    return {
        "easy": easyocr.Reader(["ko", "en"], gpu=False),
        "paddle": PaddleOCR(lang="korean",
                            show_log=False,
                            ocr_version="PP-OCRv4",
                            structure_version="PP-StructureV2")
    }
# ------------------------------------------------------------------------------------------------
