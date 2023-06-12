import streamlit as st
import pandas as pd
import json
import os
import chardet

# Create a folder to store the JSON files
json_folder = "json_files"
os.makedirs(json_folder, exist_ok=True)

st.set_page_config(
    page_title="1er secondaire",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

col1, col2, col3 = st.columns(3)
with col2:
    st.title("1er secondaire")
st.write("---")
st.header("Les series")

