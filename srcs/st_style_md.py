import streamlit as st


def hide_radio_value_md():
    st.markdown(
        body="""
        <style>
        div[role="radiogroup"] div[data-testid="stMarkdownContainer"]:has(p){ visibility: hidden; height: 0px; }
        </style>
        """,
        unsafe_allow_html=True)


def colorize_multiselect_options() -> None:
    colors = ["blue", "green", "orange", "red", "violet", "gray", "rainbow"]
    rules = ""
    n_colors = len(colors)

    for i, color in enumerate(colors):
        rules += f""".stMultiSelect div[data-baseweb="select"] span[data-baseweb="tag"]:nth-child({n_colors}n+{i}){{background-color: {color};}}"""

    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)
