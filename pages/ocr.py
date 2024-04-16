import os
import asyncio
import requests
import json
import numpy as np
import pandas as pd
import streamlit as st
import pytesseract
import easyocr
import torch
import cv2
from PIL import Image

from srcs.st_cache import get_ocr


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
st.set_page_config(page_title="ocr test",
                   page_icon="🔡",
                   layout="wide",
                   initial_sidebar_state="auto",)
reader = get_ocr()
if "image_list" not in st.session_state:
    st.session_state.image_list = os.listdir("pages/image/ocr")


def ocr_img_to_bgr_array(image: Image.Image):
    if image.mode == "RGB":
        return np.array(image)[..., ::-1]
    elif image.mode == "BRG":
        return np.array(image)
    else:
        ocr_img_to_bgr_array(image.convert("RGB"))


if __name__ == "__main__":
    st.title('🗒️🆗OCR test page')

    st.write(pytesseract.get_tesseract_version)
    col1, col2 = st.columns(2)

    section_height = 600

    with col1.container(height=section_height):
        selected_image = st.selectbox("image select",
                                      options=st.session_state.image_list,)
        st.image(image=f"pages/image/ocr/{selected_image}")
    with torch.no_grad():
        image_path = f"pages/image/ocr/{selected_image}"
        img = Image.open(image_path)
        w, h = img.size
        parsed_easy_data = []
        parsed_paddle_data = []
        with col2:
            scrollable_box = col2.container(height=section_height)
            with scrollable_box:
                tqdm_bar = scrollable_box.progress(0, "Text detecting...")
            cropped_len = round(h / w)
            for i in range(cropped_len):
                # RGB -> BGR
                page = ocr_img_to_bgr_array(image=img.crop((0, round(i * w), w, min(round((i+1) * w), h))))
                parsed_easy_data += reader["easy"].readtext(image=page,
                                                            decoder="greedy",
                                                            min_size=3)
                parsed_paddle_data += reader["paddle"].ocr(page,
                                                           cls=False,)[0]
                progress = i / cropped_len * 100
                tqdm_bar.progress(round(progress), text=f"{progress} % done...")
            easy_data = [data[1] for data in parsed_easy_data]
            paddle_data = [data[1][0] for data in parsed_paddle_data]
            tqdm_bar.empty()

            for t, readable_text in zip(scrollable_box.tabs(["easy", "paddle"]), [easy_data, paddle_data,]):
                t.write("\n\n".join(readable_text).replace("~", "\~"))
            # t.markdown(
            #     # pytesseract.image_to_string(
            #     #         Image.open("pages/image/ocr/test1.jpg"),
            #     #         lang="kor"
            #     #     )
            # )
