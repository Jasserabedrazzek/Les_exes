import streamlit as st
import os
from pathlib import Path
import base64
import sqlite3
import time

st.set_page_config(
    page_title="4eme secondaire",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("4eme secondaire")
st.write("---")
st.header("Upload File PDF or DOC or image")

# Function to create a folder for file uploads
def create_upload_folder(folder_name):
    upload_folder = os.path.join(os.getcwd(), folder_name)
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

# Get the folder name from the user
upload_folder_name = st.text_input("Enter the name of the folder for file uploads", "uploads")
upload_folder = create_upload_folder(upload_folder_name)

# Create a database connection
conn = sqlite3.connect('file_uploads.db')
c = conn.cursor()

# Create a table to store file details
c.execute('''CREATE TABLE IF NOT EXISTS files
             (name TEXT, data BLOB)''')
conn.commit()

# Function to save uploaded file to the database with retry mechanism
def save_file_to_db_with_retry(file):
    retries = 0
    while True:
        try:
            with open(file, 'rb') as f:
                file_data = f.read()
            file_name = Path(file).name
            c.execute("INSERT INTO files (name, data) VALUES (?, ?)", (file_name, sqlite3.Binary(file_data)))
            conn.commit()
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
    c.execute("SELECT data FROM files WHERE name=?", (file_name,))
    file_data = c.fetchone()[0]
    return file_data

# Create an upload button
file = st.file_uploader("Upload files (PDF, DOC, images)", type=["pdf", "doc", "jpg", "jpeg", "png"])

if file is not None:
    file_path = os.path.join(upload_folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    save_file_to_db_with_retry(file_path)

# Display uploaded files
uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
if len(uploaded_files) > 0:
    st.header("Les séries")
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
