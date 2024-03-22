import streamlit as st


if __name__ == "__main__":
    st.title('🧬 Dep Peptide App')
    with st.sidebar:
        st.page_link("pages/cardio.py",)
        st.page_link("pages/dep_peptide.py",)
        st.page_link("pages/facial.py",)


