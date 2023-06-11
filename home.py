import streamlit as st
st.set_page_config(
    page_title="Home",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
    
)
col__1,col__2,col__3 = st.columns(3)
with col__2:
    st.title(" Bienvenu ")

st.write("---")
col_1,col_2,col_3 = st.columns(3)
with col_2:
    st.header("Choisissez votre classe.")
col1,col2,col3 = st.columns(3)
with col2:
    classes = st.selectbox(
        'votre classe.',
        ('','1er', '2eme', '3eme' , '4eme'))
    if classes != ''
        nextpage = st.button('next page')
