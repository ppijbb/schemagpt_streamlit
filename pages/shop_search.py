import asyncio
import streamlit as st
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

import requests
import json
import numpy as np
import pandas as pd

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        

open_api_url = "http://apis.data.go.kr/B553077/api/open/sdsc2"
map_addr_api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/rgeocodewgs84.json"
map_auth_api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"

headers = {
    "Content-Type": "application/json",
}
# 반경 내 상권 정보 조회 API
payload={ 
    "serviceKey": st.secrets["SERVICE_KEY"],
    "pageNo": 1,
    "numOfRows": 20,
    "radius": 500,
    "cx": 126.573301,
    "cy": 33.449826,
    "indsLclsCd": "G2",
    "indsMclsCd": "G220",
    "indsSclsCd": "G22001",
    "type": "json"
}


default_map = pd.DataFrame({
            "lat": np.random.randn(1000) / 50 + 37.566535,
            "lon": np.random.randn(1000) / 50 + 126.9779692,
            "size": np.random.randn(1000) * 50,
            "color": np.random.rand(1000, 4).tolist(),
        })



if __name__ == "__main__":
    st.title('🐶 Dog Coffee Searcher 🦮')
    with st.sidebar:
        st.page_link("pages/cardio.py",)
        st.page_link("pages/dep_peptide.py",)
        st.page_link("pages/facial.py",)
    map_con = st.expander(label="지도보기")
    with map_con:
        st.map(data=default_map,
               size='size',
               color='color',
               zoom=15,
               use_container_width=False)
        
    tools = [DuckDuckGoSearchRun(
                api_wrapper=DuckDuckGoSearchAPIWrapper(time="y",
                                                       region="kr-kr",
                                                       max_results=5,
                                                       source="text")),
             WikipediaQueryRun(
                 api_wrapper=WikipediaAPIWrapper()),
             PubmedQueryRun(),
             IonicTool().tool()] + load_tools(["arxiv"],)
    
    if query := st.chat_input(placeholder="검색",):        
        payload.update({
            "cx": 126.573301,
            "cy": 33.449826
            })
        try:
            response = requests.get(url=map_auth_api_url,
                                    params={
                                       "consumer_key": st.secrets["MAP_SERVICE_ID"],
                                       "consumer_secret": st.secrets["MAP_SECRET_KEY"],
                                    })
            access_token = response.json()["result"]["accessToken"]
            response = requests.get(url=f"{map_addr_api_url}", 
                                    headers=headers, 
                                    params={
                                        "accessToken": access_token,
                                        "x_coor": 126.9779692,
                                        "y_coor": 37.566535
                                    })

            location = response.json()
        except Exception as e:
            st.write("위치 검색 오류")
            location = []

        if bool(location):
            loc_info = location["result"][0]
            # st.write(loc_info)
            query = f'{loc_info["sido_nm"]} {loc_info["sgg_nm"]} {query}'
            payload.update({
                "cx": 126.9779692,
                "cy": 37.566535
                })
        try:
            response = requests.get(url=f"{open_api_url}/storeListInRadius?", 
                                    headers=headers, 
                                    params=payload)
            # st.write(response.text)
            shops = response.json()['body']['items']
        except Exception as e:
            st.write("상점 검색 오류")
            shops = []
        # st.markdown(shops.__len__())
        if bool(shops):
            # st.write(shops)
            for s in shops:
                search_query = f'{query} {s["bizesNm"]}'
                st.markdown(search_query)
                for result in tools[0].invoke(search_query).split("..."):
                    st.markdown(result)
                    st.markdown("---")
        