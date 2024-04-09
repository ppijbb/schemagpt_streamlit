import streamlit as st
import streamlit.components.v1 as components

from streamlit_pdf_viewer import pdf_viewer

from srcs.st_cache import get_or_create_eventloop


st.set_page_config(page_title="icu challenge",
                   page_icon="🏥",
                   layout="wide",
                   initial_sidebar_state="expanded",)


if __name__ == "__main__":
    st.title('🏥 SNUBH-AWS ICU Datathon')

    st.write("응급실 데이터 분석")
    st.write("흉부 X-ray 데이터 및 환자의 혈액, 심박 등 정형 데이터 통합형 multi modal classifier")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("수상 내역")
        pdf_viewer("pages/image/icu_challenge/SNUBH.PDF", width=400, height=700)
    with col2:
        components.iframe("https://snubh-hackathon.com/", height=700, scrolling=True)
