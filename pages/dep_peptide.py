import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from srcs.st_cache import get_or_create_eventloop


if __name__ == "__main__":
    st.set_page_config(page_title="peptide",
                       page_icon="🧬",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('🧬 Dep Peptide App')

    st.markdown('''
                
        ## 프로젝트 소개
        
            고령호발질환 예측 및 진단 시스템 실증 및 실용화 연구 연계 연구
            MRM 분석을 통해 19개 우울증 후보 바이오마커 peptide 분석
            기존 바이오마커 연구팀에서 우울증 바이오마커 후보군으로 선정한 목록에 대한 분석
            연구팀 선정 바이오마커 후보 이외의 바이오마커 후보 추가 제시
            참여 기관들의 사정으로 연구 및 과제 진행은 무산됨


        ## 개발 내용
        - 우울증 진단 환자 대상 약물 치료 이후 우울증 증상이 있는 그룹(ADT), 없는 그룹(ART), 대조군 그룹에 대한 단백체 분석
        - 새로운 데이터의 중증도 평가를 위해서는 분류된 클래스가 필요, 이를 위한 knn 분류 모델 학습
        - feature 별 크기의 범위 min-max scaling 처리.
        - 모델의 추론에 대해 Feature Importance 평가
        - Random Forest, Permutation Importance, SHAP 을 이용한 핵심 feature 추출 
        - 세 가지 기법으로 대조군-ADT, 대조군-실험군, ART-ADT 사이의 차이가 있는 단백체 분석 
        - 기존 바이오 마커 후보 단백체 검출에 이어 새로운 후보 Serotransferrin 제시
        - 연구팀의 기존 연구자료에 대한 추가 MRM 분석 비교 연구
        - 추가 연구를 위한 단백체 분석 자동화 라이브러리 형태로 사내 활용
 

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=black">
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        ''', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("결과 Report 예시")
    pdf_viewer("pages/image/dep_peptide/DepressReport.pdf", width=450, height=300)
