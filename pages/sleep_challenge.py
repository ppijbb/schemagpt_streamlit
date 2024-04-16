import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from srcs.st_cache import get_or_create_eventloop


if __name__ == "__main__":
    st.set_page_config(page_title="sleep challenge",
                   page_icon="🛌",
                   layout="wide",
                   initial_sidebar_state="auto",)
    st.title('🛌 SNUBH sleep challenge')

    st.write("수면 중 수면 무호흡증 판별 대회")
    st.write("수면 중 상태로 수집되는 움직임, 심박, 코골이 소리 등의 데이터 분석")
    st.write("")
    st.markdown("---")
    st.markdown("최종 9등")
    pdf_viewer("pages/image/dep_peptide/DepressReport.pdf", width=450, height=300)
