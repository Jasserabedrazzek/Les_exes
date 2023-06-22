import streamlit as st
import os
import base64
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('uploads.db')
c = conn.cursor()

# Create the 'uploads' table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS uploads
             (file_name TEXT, file_data BLOB)''')

# Function to save file to the database
def save_file_to_db(file):
    file_data = file.read()
    file_name = file.name
    c.execute("INSERT INTO uploads (file_name, file_data) VALUES (?, ?)", (file_name, file_data))
    conn.commit()

# Function to retrieve all uploaded files from the database
def get_uploaded_files():
    c.execute("SELECT file_name FROM uploads")
    files = c.fetchall()
    return files

# Function to download a file from the database
def download_file(file_name):
    c.execute("SELECT file_data FROM uploads WHERE file_name=?", (file_name,))
    file_data = c.fetchone()[0]
    b64_data = base64.b64encode(file_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64_data}" download="{file_name}">Download</a>'

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire Pdf",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main title
st.title('Bac 2024 doc')

# File upload section
file = st.file_uploader("Upload PDF, DOC, or Image", type=["pdf", "doc", "jpeg", "jpg", "png"])

# Upload the file and save it to the database
if file is not None:
    save_file_to_db(file)
    st.success('File uploaded successfully!')

# Show uploaded files
uploaded_files = get_uploaded_files()
if uploaded_files:
    st.subheader('Uploaded Files')
    for file in uploaded_files:
        file_name = file[0]
        st.write(file_name)
        st.markdown(download_file(file_name), unsafe_allow_html=True)
else:
    st.subheader('No files uploaded yet.')
