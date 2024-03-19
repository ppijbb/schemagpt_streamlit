import streamlit as st
from srcs.cardio import heq, scale_severity

st.title('🫀 Cardioheq')
with st.sidebar:
    st.page_link("pages/cardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)


