import os
import pickle
import asyncio

import streamlit as st
from tensorflow.keras.models import model_from_json
import inspect
import cv2
import pandas as pd
from xgboost import XGBClassifier
from transformers import pipeline
import shap
import easyocr
import paddle
from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter
from langchain_community.vectorstores import Chroma

import chromadb
from chromadb.utils import embedding_functions as ef

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


@st.cache_resource
def get_facial_processors(path: str):
    # load model
    model = model_from_json(open(f"{path}/pages/rtc/caer_face.json", "r").read())
    # load weights
    model.load_weights(f"{path}/pages/rtc/caer_face.h5")

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

    def get_audio_tag(self, path:str)->dict:
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
    audio_file_list = [f"{base_path}/{filename}" for filename in os.listdir(base_path)]:
    audio_collection.add(
        ids=[get_file_name(item) for item in file_list],
        documents=audio_file_list,
        metadatas=[get_audio_tag(item) for item in file_list]
    )

    return Chroma(
        collection_name="mfcc_dtw_collection",
        client=audio_vector_db,
        embedding_function=ef.MFCCEmbeddingFunction() # Custom Audio Embedding function
        ).as_retriever()


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


@st.cache_resource
def get_ocr():
    return {
        "easy": easyocr.Reader(["ko", "en"], gpu=False),
        "paddle": PaddleOCR(lang="korean",
                            show_log=False,
                            ocr_version="PP-OCRv4",
                            structure_version="PP-StructureV2")
    }


