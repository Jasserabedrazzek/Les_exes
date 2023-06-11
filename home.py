import streamlit as st

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
        background-image: url('path_to_your_image');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col__1, col__2, col__3 = st.columns(3)
with col__2:
    st.title(" Bienvenu ")

st.write("---")
col_1, col_2, col_3 = st.columns(3)
with col_2:
    st.header("Choisissez votre classe.")

col1, col2, col3 = st.columns(3)
with col2:
    classes = st.selectbox(
        'votre classe.',
        ('', '1er', '2eme', '3eme', '4eme')
    )
    if classes != '':
        nextpage = st.button('next page')
        if nextpage:
            if classes == '1er':
                pass
            elif classes == '2eme':
                pass
            elif classes == '3eme':
                pass
            elif classes == '4eme':
                pass
st.write("---")

st.markdown("Copyright © 2023 [Edu](#) . All Rights Reserved.")
