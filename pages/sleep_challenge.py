import streamlit as st
from streamlit_pdf_viewer import pdf_viewer


if __name__ == "__main__":
    st.set_page_config(page_title="sleep challenge",
                       page_icon="🛌",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('🛌 SNUBH Medical AI Challenge 2022')

    st.markdown('''
                
        ## 프로젝트 소개
        
            수면 중 수면 무호흡증 판별 대회 참여
            자가 수면 검사 데이터 움직임, 심전도, 호흡음을 이용한 수면 무호흡증 리스크 예측 대회
            참가 66팀 중 최종 9등 달성

        ## 개발 내용
        - 수면 중 측정된 자가 수면 검사 데이터 분석
        - 각 데이터는 6시간 가량의 생체신호 (액티그래피, 심전도, 수면 중 녹음된 소리)
        - 시계열 EDF 데이터 train+val 300 건 test 102건
        - 수면 무호흡증의 판독은 수면 다원검사 결과 1시간 당 무호흡/저호흡 발생이 5회 이상인 경우
        - 6시간 데이터를 1시간 단위 샘플링을 통한 데이터 증강 300건 -> 1500 건
        - 액티그래프, ECG, Mel Spectrogram 데이터를 입력받아 학습하는 CNN 모델 설계 및 학습
 

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=black">       
        <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
        <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=black">
        <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=black">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        ''', unsafe_allow_html=True)
    
    # pdf_viewer("pages/image/dep_peptide/DepressReport.pdf", width=450, height=300)
