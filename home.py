import streamlit as st
import webbrowser


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded"
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
        ('Votre classe.', '1er', '2eme', '3eme', '4eme')
    )
    if classes != ['1er', '2eme', '3eme', '4eme']:
        
        if classes == '1er':
            url = "https://1er-secondaire.streamlit.app/"
            st.markdown(f'<a href="{url}" target="_blank">1er secondaire</a>', unsafe_allow_html=True)# Execute 1er.py
        elif classes == '2eme':
            url = "https://2eme-secondaire.streamlit.app/"
            st.markdown(f'<a href="{url}" target="_blank">2eme secondaire</a>', unsafe_allow_html=True)
        elif classes == '3eme':
            url = "https://3eme-secondaire.streamlit.app/"
            st.markdown(f'<a href="{url}" target="_blank">3eme secondaire</a>', unsafe_allow_html=True)
        elif classes == '4eme':
            url = "https://4eme-secondaire.streamlit.app/"
            st.markdown(f'<a href="{url}" target="_blank">4eme secondaire</a>', unsafe_allow_html=True)
            
st.write("---")
st.markdown("Copyright © 2023 [Edu](#) . All Rights Reserved.")
