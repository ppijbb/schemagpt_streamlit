import asyncio
import requests
import json
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk

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
                                           SerpAPIWrapper, WikipediaAPIWrapper)
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from langchain_openai import ChatOpenAI
from ionic_langchain.tool import IonicTool
from langchain_community.llms.fake import FakeStreamingListLLM

from srcs.st_cache import get_or_create_eventloop
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


open_api_url = "http://apis.data.go.kr/B553077/api/open/sdsc2"
map_addr_api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/rgeocodewgs84.json"
map_loca_api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocodewgs84.json"
map_auth_api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"

if 'lat' not in st.session_state:
    st.session_state.lat = 37.566535 # 33.449826 # 
if 'lon' not in st.session_state:
    st.session_state.lon = 126.9779692 # 126.573301 # 
if 'map' not in st.session_state:
    st.session_state.map = pd.DataFrame(
        {
            "lat": np.random.randn(10) / 10 + st.session_state.lat,
            "lon": np.random.randn(10) / 10 + st.session_state.lon,
            "size": np.random.randn(10),
            "height": np.random.randn(10),
            "color": np.random.rand(10, 4).tolist(),
        }
    )




if __name__ == "__main__":
    st.set_page_config(page_title="schedule scrapper",
                       page_icon="🏪",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('🐶 Idol Schedule Scrapper ')
    st.markdown('''            
        ## 프로젝트 소개
        
            아이돌 스케줄 웹 스크래핑
            

        ## 개발 내용
        - 공식 일정 찾아오는 스크래퍼 만들기

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        ''', unsafe_allow_html=True)
    
    # Selenium web scraping
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get("https://www.example.com")

    # Get the HTML content
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content
    # Use your preferred HTML parsing library here
    # For example, you can use BeautifulSoup

    # Extract the desired information from the parsed HTML
    # For example, you can find elements by tag name, class, or id
    # and extract their text or attributes
