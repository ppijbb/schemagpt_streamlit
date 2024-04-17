import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from srcs.st_cache import get_or_create_eventloop


if __name__ == "__main__":
    st.set_page_config(page_title="peptide",
                       page_icon="🧬",
                       layout="wide",
                       initial_sidebar_state="auto",)
    st.title('🧬 Dep Peptide App')

    st.write("우울증 진단 환자 대상 약물 치료 이후 증상이 있는 그룹, 없는 그룹, 대조군 그룹에 대한 단백체 분석")
    st.write("MRM 분석을 통해 19개 우울증 후보 바이오마커 peptide 분석")
    st.write("")
    st.markdown("---")
    st.markdown("결과 Report 예시")
    pdf_viewer("pages/image/dep_peptide/DepressReport.pdf", width=450, height=300)
