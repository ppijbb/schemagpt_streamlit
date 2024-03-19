import os
import streamlit as st
from srcs.cardio import heq, scale_severity
import streamlit.components.v1 as components


os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "1"

st.title('🫀 Cardio')
with st.sidebar:
    st.page_link("pages/cardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)

with open(os.getcwd()+"/static/views/index.html", "r") as f:
    components.html(f.read())
