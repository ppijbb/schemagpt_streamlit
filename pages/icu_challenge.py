import streamlit as st
import streamlit.components.v1 as components

from streamlit_pdf_viewer import pdf_viewer


if __name__ == "__main__":
    st.set_page_config(page_title="icu challenge",
                       page_icon="🏥",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('🏥 SNUBH-AWS ICU Datathon')

    st.markdown('''

        ## 프로젝트 소개

            응급실 데이터 분석
            흉부 X-ray 데이터 및 환자의 혈액, 심박 등 정형 데이터 통합형 multi-modal ensemble modal classifier
            예선 MIMIC 데이터 분석 평가를 통과한 팀대상 본선 ICU 데이터 분석 진행
            성별, 연령에 대한 인공지능의 편향성에 대한 평가와 성능에 대해 종합 평가 진행
            예선 30팀 중 본선 진출 4등 달성

        ## 개발 내용
        - 중환자실에서 발생하는 데이터 분석을 통해 입원 기간 및 사망여부 예측 모델
        - 사망 직전의 데이터가 라벨에 대한 가장 확실한 기준을 제시 가능하지만 실질적인 활용은 의미 없음
        - 중환자실 입원 초기 환자의 정보로 환자에 대한 의료진의 판단 보조에 활용할 수 있도록 설계
        - 어느 환자에게 얼만큼의 인적·물적 자원을 할당해야 하는지 판단 가능하게 하는 것을 목표 
        
        ### MIMIC
        - 예선 단계 미국 중환자실 데이터 Medical Information Mart For Intensive Care III (MIMIC-III) 데이터 분석 내용 평가
        - 흉부 X-ray, ECG, 중환자실에서 수집된 환경 및 생체 데이터 등의 정형 데이터를 활용한 multi-modal 학습
        - 제공된 정형 데이터 중 기존 연구 레퍼런스 참고하여 의미가 있는 feature 추출 
        - X-ray 데이터는 efficient net-b4 를 이용해 featrue 추출
        
        ### ICU Dataset
        - 본선 단계 분당 서울대 병원 데이터 분석 내용 평가
        - MIMIC 데이터와 동일한 구조이나 활용 가능한 데이터는 X-ray와 정형데이터
        - X-ray 데이터를 학습한 efficient net-b4와 CatBoost, GradientBoost, LGBM, XGBoost, Gaussian NB 의 Ensemble 모델 학습     
        

        ## 사용 기술
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
        <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=black">       
        <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=black">
        <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=black">
        <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=black"> 
        <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
        <img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=black">
        ''', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("수상 내역")
        pdf_viewer("pages/image/icu_challenge/SNUBH.PDF", width=400, height=700)

    with col2:
        components.iframe("https://snubh-hackathon.com/", height=700, scrolling=True)
    st.markdown("Final Ensemble Model structure")
    st.image("pages/image/icu_challenge/icu_model.png")
    st.markdown("Explaining Ensemble Model Inference with SHAP")
    st.image("pages/image/icu_challenge/icu_shap.png")
