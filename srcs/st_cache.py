import streamlit as st
from tensorflow.keras.models import model_from_json
import inspect
import cv2
import os
import pickle
import pandas as pd
from xgboost import XGBClassifier
from transformers import pipeline
import asyncio
import shap
import easyocr
import paddle
from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma


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
    return cgi_classifier, shap.Explainer(cgi_classifier)


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
        "easy": easyocr.Reader(["ko", "en"]),
        "paddle": PaddleOCR(lang="korean",
                            show_log=False,
                            ocr_version="PP-OCRv4",
                            structure_version="PP-StructureV2")
    }


