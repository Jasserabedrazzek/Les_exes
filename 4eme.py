import streamlit as st
import os
from pathlib import Path
import base64
import sqlite3
import time

st.set_page_config(
    page_title="4eme secondaire",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Bac 2024")
st.write("---")
st.header("Upload Files PDF or Doc ")

upload_folder = "uploads"
os.makedirs(upload_folder, exist_ok=True)

# Function to save uploaded file to the database with retry mechanism
def save_file_to_db_with_retry(file_path, file_name, file_data):
    retries = 0
    while True:
        try:
            with sqlite3.connect('file_uploads.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO files (name, data) VALUES (?, ?)", (file_name, sqlite3.Binary(file_data)))
            st.success("File uploaded successfully.")
            break
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e).lower() and retries < 5:
                retries += 1
                delay = 2 ** retries  # exponential backoff
                st.warning(f"Database is locked. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                st.error("Failed to upload file. Please try again later.")
                break

# Function to retrieve file from the database
def retrieve_file_from_db(file_name):
    with sqlite3.connect('file_uploads.db') as conn:
        c = conn.cursor()
        c.execute("SELECT data FROM files WHERE name=?", (file_name,))
        row = c.fetchone()
        if row is not None:
            file_data = row[0]
            return file_data
        else:
            return None

# Create a database connection and table if not exists
with sqlite3.connect('file_uploads.db') as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (name TEXT, data BLOB)''')

# Create an upload button
file = st.file_uploader("Upload files (PDF, DOC)", type=["pdf", "doc"])

if file is not None:
    file_path = os.path.join(upload_folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    save_file_to_db_with_retry(file_path, file.name, file.getbuffer())

# Display uploaded files
uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
if len(uploaded_files) > 0:
    st.header("Les séries")
    for uploaded_file in uploaded_files:
        file_data = retrieve_file_from_db(uploaded_file)
        if file_data is not None:
            st.write(uploaded_file)
            download_button = st.button("Download", key=uploaded_file)
            if download_button:
                b64_data = base64.b64encode(file_data).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{uploaded_file}">Click to download</a>'
                st.markdown(href, unsafe_allow_html=True)

st.write("---")
st.markdown("Copyright © 2023 [Edu](#) . All Rights Reserved.")
