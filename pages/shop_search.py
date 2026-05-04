import requests
import json
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from srcs.st_cache import get_or_create_eventloop

get_or_create_eventloop()


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


MAP_MAX_ROWS = 500


def add_pin_in_map(lat: float, lon: float, size: float, color: float):
    st.session_state.map = pd.concat([
        st.session_state.map,
        pd.DataFrame({
            "lat": lat,
            "lon": lon,
            "size": size,
            "height": np.random.randn(1),
            "color": color
        })
    ], ignore_index=True).drop_duplicates(subset=["lat", "lon"], keep="last")
    if len(st.session_state.map) > MAP_MAX_ROWS:
        st.session_state.map = st.session_state.map.tail(MAP_MAX_ROWS).reset_index(drop=True)


headers = {
    "Content-Type": "application/json",
}
# 반경 내 상권 정보 조회 API
payload = {
    "serviceKey": st.secrets["SERVICE_KEY"],
    "pageNo": 1,
    "numOfRows": 20,
    "radius": 500,
    "cx": st.session_state.lon,
    "cy": st.session_state.lat,
    "indsLclsCd": "G2",
    "indsMclsCd": "G220",
    "indsSclsCd": "G22001",
    "type": "json"
}


if __name__ == "__main__":
    st.set_page_config(page_title="shop search",
                       page_icon="🏪",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('🐶 Dog Coffee Searcher 🦮')
    st.markdown('''            
        ## 프로젝트 소개
        
            위치기반 애견 관련 사업체 탐색 프로젝트
            검색하는 위치의 애견 카페 또는 애견 미용실 등의 정보 제공
            

        ## 개발 내용
        - 상가정보 조회 API에서 특정위치의 특정 업종의 업체 목록 조회
        - DuckDuckGO 엔진에서 업체별 정보 수집
        - 상가 주소 좌표 변환 통계청 API 결과로 지도 시각화
        - 지도상에 시각화
        - 각 업체별 리뷰, 정보 제공

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        ''', unsafe_allow_html=True)
    # with st.sidebar:
    #     st.page_link("pages/cardio.py",)
    #     st.page_link("pages/dep_peptide.py",)
    #     st.page_link("pages/facial.py",)
    
    map_section, search_section = st.columns(2)
    with map_section:
        # map_con = st.expander(label="지도보기")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/outdoors-v11',
            initial_view_state=pdk.ViewState(
                latitude=st.session_state.lat,
                longitude=st.session_state.lon,
                zoom=15,
                pitch=65,
                bearing=15,
            ),
            tooltip={"html": "value: {height}"},
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=st.session_state.map,
                    get_position=['lon', 'lat'],
                    get_fill_color=[200, 30, 0, 160],
                    radius=20,
                    get_elevation_weight="height",
                    elevation_scale=5,
                    elevation_range=[0, 100],
                    pickable=True,
                    extruded=True,
                    auto_highlight=True,
                    coverage=1
                ),
                # pdk.Layer(
                #     'ScatterplotLayer',
                #     data=st.session_state.map,
                #     get_position='[lon, lat]',
                #     get_color='[200, 30, 0, 160]',
                #     get_radius=200,
                # ),
            ],
        ))
        x = st.number_input(label='x',
                            key="lon",
                            step=0.0000001,
                            format="%.7f",)
        y = st.number_input(label='y',
                            key="lat",
                            step=0.000001,
                            format="%.6f",)        
    #    with map_con:
     
    with search_section:
        tools = [DuckDuckGoSearchRun(
                    api_wrapper=DuckDuckGoSearchAPIWrapper(time="y",
                                                           region="kr-kr",
                                                           max_results=5,
                                                           source="text")),
                 WikipediaQueryRun(
                     api_wrapper=WikipediaAPIWrapper()),
                 PubmedQueryRun(),
                #  IonicTool().tool()
                 ] + load_tools(["arxiv"],)
        
        if query := st.chat_input(placeholder="검색",):        
            payload.update({
                "cx": st.session_state.lon,
                "cy": st.session_state.lat
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
                                            "x_coor": str(st.session_state.lon),
                                            "y_coor": str(st.session_state.lat),
                                            "addr_type": str(10)
                                        })
                location = response.json()
                assert location["errCd"] == 0, location["errMsg"]
            except Exception as e:
                st.write(f"위치 검색 오류: {e}")
                location = []

            if bool(location):
                loc_info = location["result"][0]
                # st.write(loc_info)
                query = f'{loc_info["sido_nm"]} {loc_info["sgg_nm"]} {query}'
                payload.update({
                    "cx": st.session_state.lon,
                    "cy": st.session_state.lat
                    })
            try:
                response = requests.get(url=f"{open_api_url}/storeListInRadius?", 
                                        headers=headers, 
                                        params=payload)
                # st.write(response.text)
                shops = response.json()['body']['items']
            except Exception as e:
                st.write(f"상점 검색 오류: {e}")
                shops = []

            if bool(shops):
                for s in shops:
                    add_pin_in_map(lat=s["lat"],
                                   lon=s["lon"],
                                   size=np.random.rand(1),
                                   color=np.random.rand(1, 4).tolist())
                    search_query = f'{s["bizesNm"]} {query}'
                    st.markdown(f'> {search_query}')
                    for result in tools[0].invoke(search_query).split("..."):
                        st.text_area('', f'{result}')
                        st.markdown("---")
            else:
                st.markdown("검색 결과가 없습니다")

    st.divider()

