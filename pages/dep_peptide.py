import streamlit as st

st.title('🧬 Dep Peptide App')
with st.sidebar:
    st.page_link("pages/staticscardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)

st.write(st.session_state["shared"])
