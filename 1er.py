import streamlit as st
import os
from pathlib import Path
import base64
import sqlite3

st.set_page_config(
    page_title="1er secondaire",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("1er secondaire")
st.write("---")
st.header("Les séries")

upload_folder = "uploads"
os.makedirs(upload_folder, exist_ok=True)

# Create a database connection
conn = sqlite3.connect('file_uploads.db')
c = conn.cursor()

# Create a table to store file details
c.execute('''CREATE TABLE IF NOT EXISTS files
             (name TEXT, data BLOB)''')
conn.commit()

# Function to save uploaded file to the database
def save_file_to_db(file):
    with open(file, 'rb') as f:
        file_data = f.read()
    file_name = Path(file).name
    c.execute("INSERT INTO files (name, data) VALUES (?, ?)", (file_name, sqlite3.Binary(file_data)))
    conn.commit()

# Function to retrieve file from the database
def retrieve_file_from_db(file_name):
    c.execute("SELECT data FROM files WHERE name=?", (file_name,))
    file_data = c.fetchone()[0]
    return file_data

# Create an upload button
file = st.file_uploader("Upload files (PDF, DOC, images)", type=["pdf", "doc", "jpg", "jpeg", "png"])

if file is not None:
    file_path = os.path.join(upload_folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    save_file_to_db(file_path)
    st.success("File uploaded successfully.")

# Display uploaded files
uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
if len(uploaded_files) > 0:
    st.header("Uploaded Files")
    for uploaded_file in uploaded_files:
        file_data = retrieve_file_from_db(uploaded_file)
        st.write(uploaded_file)
        download_button = st.button("Download", key=uploaded_file)
        if download_button:
            b64_data = base64.b64encode(file_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{uploaded_file}">Click to download</a>'
            st.markdown(href, unsafe_allow_html=True)
st.write("---")
st.markdown("Copyright © 2023 [Edu](#) . All Rights Reserved.")
