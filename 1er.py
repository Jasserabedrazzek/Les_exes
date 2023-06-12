import streamlit as st
import pandas as pd
from io import StringIO
import json

st.set_page_config(
    page_title="1er secondaire",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

col1,col2,col3 = st.columns(3)
with col2 :
  st.title("1er secondaire")
  st.write("---")
  st.header("Les series")
  
  
  
  st.write("---")
  uploads = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
