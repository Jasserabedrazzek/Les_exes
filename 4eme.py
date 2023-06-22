import streamlit as st
import os
import shutil
from PIL import Image
import sqlite3

# Create a directory to store uploaded files
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire Pdf",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Create a database connection
conn = sqlite3.connect("urls.db")
c = conn.cursor()

# Create a table to store URLs if it doesn't exist
c.execute("CREATE TABLE IF NOT EXISTS urls (url TEXT)")

# Function to handle file uploads
def handle_file_upload(file, file_type):
    file_name = file.name
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    if file_type == "pdf" or file_type == "doc":
        st.success(f"File uploaded: {file_name}")
    elif file_type == "image":
        st.success(f"Image uploaded: {file_name}")

# Function to download a file
def download_file(file_path, file_name):
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    st.download_button("Download", file_bytes, file_name)

# Function to save URL in the database
def save_url(url):
    c.execute("INSERT INTO urls (url) VALUES (?)", (url,))
    conn.commit()
    st.success("URL saved successfully!")

# Display the title
st.title('Bac 2024 doc')

# Display the URL input field and save button
url = st.text_input("Enter a URL:")
if st.button("Save URL") and url:
    save_url(url)

# Display the upload buttons
file_type = st.radio("Select file type:", ("pdf", "doc", "image"))
file = st.file_uploader(f"Upload {file_type.capitalize()} file")
if file is not None:
    handle_file_upload(file, file_type)

# Display the uploaded files
uploaded_files = os.listdir(UPLOAD_DIRECTORY)
st.subheader("Uploaded Files")
for file_name in uploaded_files:
    st.write(file_name)
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    if file_name.endswith(".pdf") or file_name.endswith(".doc"):
        download_file(file_path, file_name)
    elif file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
        image = Image.open(file_path)
        st.image(image)
        download_file(file_path, file_name)

# Close the database connection
conn.close()
