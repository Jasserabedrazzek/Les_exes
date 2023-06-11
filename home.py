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
col1,col2,col3,col4 = st.columns(4)
with col1:
    button_style = """
        <style>
            .button-width {
        width: 150px;
            }
        </style>
        """

# Display the CSS style
    st.markdown(button_style, unsafe_allow_html=True)
    class1 = st.button(" 1er ", key="button1", help="Click me!")
