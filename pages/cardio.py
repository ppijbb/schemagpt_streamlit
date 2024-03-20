import os
import sys
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "1"

import streamlit as st
from srcs.cardio import heq, scale_severity
import streamlit.components.v1 as components


# st.set_page_config(layout="wide")
st.title('🫀 Cardio')
with st.sidebar:
    st.page_link("pages/cardio.py",)
    st.page_link("pages/dep_peptide.py",)
    st.page_link("pages/facial.py",)


@st.cache_resource
def add_static_js():
    js_dir = f"{os.getcwd()}/static/css"
    js_file_list = [dir for dir in os.listdir(js_dir) if dir.endswith("2.css")]

    js_data = ""

    for js in js_file_list:
        with open(f"{js_dir}/{js}", "r") as f:
            js_data += f'<style>\n{f.read()}\n</style>\n'
    return js_data


with (open(os.getcwd()+"/static/views/index.html", "r") as f):
    html_obj = f'{f.read()}'
    # html_obj = html_obj.replace("text/javascript", "applcation/javascript")
    # html_obj = html_obj.replace("text/css", "text/html")
    # st.markdown(add_static_js(), unsafe_allow_html=True)
    main_component = components.html(html_obj, scrolling=True, height=700)

    f'''
    {main_component.__dir__()}
    '''

