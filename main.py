__import__('pysqlite3')
import os
import asyncio
import sys
import copy
import signal
import time
import json
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "0"

from srcs.app_static_file_handler import AppStaticFileHandler

sys.modules["streamlit.web.server.app_static_file_handler"].AppStaticFileHandler = AppStaticFileHandler

import pandas as pd
import streamlit as st

from streamlit_option_menu import option_menu

from langchain.callbacks.manager import CallbackManager
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType, ConversationalChatAgent, AgentExecutor, Tool
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler

from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.tools import DuckDuckGoSearchRun, BingSearchRun, WikipediaQueryRun
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import (DuckDuckGoSearchAPIWrapper, GoogleSearchAPIWrapper, BingSearchAPIWrapper,
                                           SerpAPIWrapper, WikipediaAPIWrapper, PubMedAPIWrapper)
# from langchain_community.utilities.pubmed import PubMedAPIWrapper

from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from langchain_openai import ChatOpenAI
from ionic_langchain.tool import IonicTool

from srcs import schema_therapy
from srcs.st_cache import get_utterance_data, get_or_create_eventloop



loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


if __name__ == "__main__":
    st.set_page_config(page_title="main",
                    page_icon="👋",
                    layout="wide",
                    initial_sidebar_state="auto",)

    st.title('👋😄 Welcome!')
    if "shared" not in st.session_state:
        st.session_state["shared"] = True

    with st.sidebar:
        side1, side2, side3 = st.columns(3)
        # option_menu("Main Menu", ["Home", 'Settings'], 
        # icons=['house', 'gear'], menu_icon="cast", default_index=1)
        side1.markdown("[![github](https://img.icons8.com/?size=24&id=fmFqQmR0UdsR&format=png)](https://github.com/ppijbb)")
        side2.markdown("[![LinkedIn](https://img.icons8.com/?size=24&id=13930&format=png)](https://www.linkedin.com/in/권환-정-ba37b122b)")
        side3.markdown("[![Gmail](https://img.icons8.com/?size=24&id=37246&format=png)](mailto:ppijbb@gmail.com)")
    
    st.markdown("""
      # 안녕하세요! 정권환입니다.

      헬스케어, 디지털 바이오, 음성/오디오 데이터 분야의 경험을 넓히고 있는
      
      데이터 분석, AI 엔지니어(ML/DL) 입니다.

      데이터 분석, 모델 아키텍처, MLOps, LLM 서비스 등

      단순히 인공지능이 들어간 서비스가 아닌 도메인과 목적에 맞게 설계하고 연구합니다.

      상상만 하던 서비스를 만들어 내는 꿈을 가지고 개발하고 연구하고 있습니다.

      """)

    section1, section2 = st.columns(2)
    with section1:
      st.markdown("### 🎓 EDUCATION")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2011.03~2014.02")
      inc.markdown("###### 노원 고등학교")
      # inc.markdown("-")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2014.03~2021.02")
      inc.markdown("###### 가천대학교")
      inc.markdown("글로벌 캠퍼스 컴퓨터공학과")

      st.markdown("### 💻 WORK EXPERIENCE")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2020.02~2020.06")
      inc.markdown("###### ㈜휴레이포지티브")
      inc.markdown("기업부설연구소 인턴 연구원")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2020.09~2020.12")
      inc.markdown("###### 행정 안전부")
      inc.markdown("한국정보화진흥원 직접사업팀 인턴")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2021.04~2024.05")
      inc.markdown("###### ㈜튜링바이오") 
      inc.markdown("연구소 연구원")
      inc.markdown("연구소 선임 연구원")

      st.markdown("### 🏆 AWARDS")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2023.09~2023.10")
      inc.markdown("###### 분당 서울대 병원") 
      inc.markdown("SNUBH-AWS ICU Datathon 4등상")

      st.markdown("### 📜 CERTIFICATION")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2018.06")
      inc.markdown("###### 네트워크 관리사 2급") 
      inc.markdown("한국정보통신자격협회")
      years, inc = st.columns([0.4, 0.6])
      years.markdown("###### 2019.10")
      inc.markdown("###### 빅데이터분석 실무 2급") 
      inc.markdown("한국정보인재개발원")

    with section2:
      st.markdown("### 📚 SKILLS")
      st.markdown('''
  <div style="font-family:'Roboto'; font-size: 16px; font-weight: 400; color: black; font-weight: bold;">
    Language <br>
      <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
      <img src="https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=black"> 
    <br>
    Database<br>
      <img src="https://img.shields.io/badge/dynamodb-4053D6?style=for-the-badge&logo=0175C2&logoColor=white"> 
      <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
      <img src="https://img.shields.io/badge/postgresql-003545?style=for-the-badge&logo=postgresql&logoColor=white"> 
      <img src="https://img.shields.io/badge/mongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white">
  <!-- <img src="https://img.shields.io/badge/firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=white"> -->
    <br>
  <!--   Front<br>
      <img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black"> 
    <br> -->
    Back<br>
      <img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
      <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
      <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">  
    <br>
    Data Science<br>
      <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=black"> 
      <img src="https://img.shields.io/badge/scipy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=black">
      <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
      <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=black"> 
      <img src="https://img.shields.io/badge/plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=black"> 
    <br>
    Deep Learning<br>
      <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=black"> 
      <img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=black"> 
      <img src="https://img.shields.io/badge/keras-D00000?style=for-the-badge&logo=keras&logoColor=black"> 
      <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=black"> 
    <br>
    Version control <br>
      <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
      <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
      <img src="https://img.shields.io/badge/huggingface-FF9A00?style=for-the-badge&logo=huggingface&logoColor=white">
    <br>
    Environ<br>
      <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"> 
      <img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=black"> 
      <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=black"> 
    <br>
    Cloud<br>
      <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> 
      <img src="https://img.shields.io/badge/googlecloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"> 
    <br>
    Etc<br>
      <img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=black"> 
      <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=black"> 
      <img src="https://img.shields.io/badge/webrtc-333333?style=for-the-badge&logo=webrtc&logoColor=white">
    <br>
  </div>
      ''',
      unsafe_allow_html=True)
