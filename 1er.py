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
if uploads:
        for file in uploads:
            df = pd.read_csv(file)
            # Convert DataFrame to JSON
            json_data = df.to_json(orient='records')
            # Save JSON data to a file
            filename = f"{file.name.split('.')[0]}.json"
            with open(filename, 'w') as f:
                f.write(json_data)
            st.write(f"File saved as {filename}")
  
    # Display the uploaded files
    uploaded_files = [file for file in os.listdir() if file.endswith('.json')]
    for file in uploaded_files:
        with open(file, 'r') as f:
            json_data = f.read()
        st.write("### File:", file)
        # Parse JSON data
        df = pd.read_json(json_data)
        st.dataframe(df)
