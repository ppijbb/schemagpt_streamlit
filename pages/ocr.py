import asyncio
import requests
import json
import numpy as np
import pandas as pd
import streamlit as st
import pytesseract
import easyocr
import torch
from PIL import Image

from srcs.st_cache import get_ocr


st.set_page_config(page_title="ocr test",
                   page_icon="🔡",
                   layout="wide",
                   initial_sidebar_state="expanded",)
reader = get_ocr()

if __name__ == "__main__":
    st.title('🗒️🆗OCR test page')

    st.write(pytesseract.get_tesseract_version)
    col1, col2 = st.columns(2)

    with col1.container(height=200):
        st.image(image="pages/image/ocr/test1.jpg")
    with torch.no_grad():
        parsed_data = reader.readtext("pages/image/ocr/test1.jpg")
        readable_text = [data[1] for data in parsed_data]
        col2.markdown(
            "\n".join(readable_text)
        )
        col2.divider()
        col2.markdown(
            pytesseract.image_to_string(
                    Image.open("pages/image/ocr/test1.jpg"),
                    lang="kor"
                )
        )
