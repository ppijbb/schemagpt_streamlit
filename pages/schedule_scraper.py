import asyncio
import requests
import json
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk

import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def get_month(date=(datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%Y%m")):
    year = int(date[:4])
    month = int(date[4:])
    return f"{year}{month:02d}"


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
    
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--incognito")  # Enable incognito mode
    options.add_argument('--disable-gpu') # Disable the GPU acceleration
    options.add_argument('--log-level=3') # Disable the log
    driver = webdriver.Chrome(options=options)

    # Selenium web scraping
    timer = st.progress(0, "wait for loading")
    for i in range(100):
        time.sleep(0.03)
        timer.progress(i+1, "wait for loading")
    
    # Open the webpage
    driver.get(f"https://blip.kr/schedule/{get_month()}")
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "footer-mobile-container")))
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    # Get the HTML content
    search_box = driver.find_elements(By.CLASS_NAME, "monthly-schedule-page-canvan-item")

    timer = st.progress(0, "process element")
    for i, result in enumerate(search_box):
        time.sleep(st.secrets["SCRAP_SEC"])
        result = result.find_element(By.CLASS_NAME, 'schedule-card-list-list')
        time.sleep(st.secrets["SCRAP_SEC"])
        element = result.find_elements(By.CLASS_NAME, 'schedule-card-container')
        for content in element:
            time.sleep(st.secrets["SCRAP_SEC"])
            schedule_title = content.find_element(By.CLASS_NAME, 'schedule-card-title')
            time.sleep(st.secrets["SCRAP_SEC"])
            schedule_date = content.find_element(By.CLASS_NAME, 'schedule-card-date')
            time.sleep(st.secrets["SCRAP_SEC"])
            schedule_artist = content.find_element(By.CLASS_NAME, 'schedule-card-artist') 
            try:
                st.markdown(f"{schedule_artist.text} {schedule_date.text} {schedule_title.text}")
            except:
                pass
        timer.progress(i+1, "process element")

    # Close the browser
    driver.quit()

    # Parse the HTML content
    # Use your preferred HTML parsing library here
    # For example, you can use BeautifulSoup

    # Extract the desired information from the parsed HTML
    # For example, you can find elements by tag name, class, or id
    # and extract their text or attributes
