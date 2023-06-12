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

uploads = st.file_uploader("Choose a file", accept_multiple_files=True)

if uploads:
    for file in uploads:
        with file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, encoding=encoding)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    st.warning(f"The file {file.name} is not supported. Please upload a CSV, XLS, or XLSX file.")
                    continue

                if df.empty:
                    st.warning(f"The file {file.name} is empty.")
                    continue
            except pd.errors.EmptyDataError:
                st.warning(f"The file {file.name} is empty or contains no columns.")
                continue

        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records')

        # Save JSON data to a file in the json_folder
        filename = f"{json_folder}/{file.name.split('.')[0]}.json"
        with open(filename, 'w') as f:
            f.write(json_data)

        st.write(f"File saved as {filename}")

    # Display the uploaded files
    uploaded_files = [file for file in os.listdir(json_folder) if file.endswith('.json')]
    for file in uploaded_files:
        with open(os.path.join(json_folder, file), 'r') as f:
            json_data = f.read()

        st.write("### File:", file)
        # Parse JSON data
        df = pd.read_json(json_data)
        st.dataframe(df)

        # Provide download link for the JSON file
        st.download_button("Download JSON", os.path.join(json_folder, file))
