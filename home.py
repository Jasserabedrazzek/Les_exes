import streamlit as st
import subprocess

st.set_page_config(
    page_title="Home",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    body {
        background-image: url('static/images/5190234.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col__1, col__2, col__3 = st.columns(3)
with col__2:
    st.title(" Bienvenue ")

st.write("---")
col_1, col_2, col_3 = st.columns(3)
with col_2:
    st.header("Choisissez votre classe.")

col1, col2, col3 = st.columns(3)
with col2:
    classes = st.selectbox(
        'Votre classe.',
        ('', '1er', '2eme', '3eme', '4eme')
    )
    if classes != '':
        nextpage = st.button('Next page')
        if nextpage:
            if classes == '1er':
                subprocess.run(["python", "1er.py"])  # Execute 1er.py
            elif classes == '2eme':
                subprocess.run(["python", "2eme.py"])  # Execute 2eme.py
            elif classes == '3eme':
                subprocess.run(["python", "3eme.py"])  # Execute 3eme.py
            elif classes == '4eme':
                subprocess.run(["python", "4eme.py"])  # Execute 4eme.py
