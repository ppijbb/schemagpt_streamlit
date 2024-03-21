import os
import sys
import streamlit as st
from srcs.cardio import heq, scale_severity
import streamlit.components.v1 as components


st.set_page_config(layout="wide",)
st.title('🧫 ZSD Organoid Detection')

with st.sidebar:
    st.page_link("pages/cardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)
    st.page_link("pages/zsd_organoid.py", )

components.iframe("https://colab.research.google.com/drive/1bEsarMLfjrRcpvAYsaYaiIfSfM4LWm1k?usp=sharing",
                  height=700)

