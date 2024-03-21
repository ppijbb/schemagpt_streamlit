import streamlit as st
from tensorflow.keras.models import model_from_json
import inspect
import cv2
import os
import pickle
import pandas as pd
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma


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
