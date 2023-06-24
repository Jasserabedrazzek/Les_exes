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
    page_icon=":blue_book:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Create a database connection
conn = sqlite3.connect("urls.db")
c = conn.cursor()

# Create a table to store URLs if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS urls (url text)''')

# Function to handle file uploads
def handle_file_upload(file):
    file_name = file.name
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    if file_name.endswith((".pdf", ".doc")):
        st.success(f"File uploaded: {file_name}")
    elif file_name.endswith((".jpg", ".jpeg", ".png")):
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

# Display the title
st.title('Bac 2024 doc')

# Display the file upload section for PDF or DOC files
st.subheader("Upload PDF or DOC")
file = st.file_uploader("Upload PDF or DOC file", accept_multiple_files=True)
if file is not None:
    for uploaded_file in file:
        handle_file_upload(uploaded_file)

# Display the file upload section for images
st.subheader("Upload Images")
file = st.file_uploader("Upload Image file", accept_multiple_files=True)
if file is not None:
    for uploaded_file in file:
        handle_file_upload(uploaded_file)

# Display the URL input and save button
url = st.text_input("Enter URL")
save_button = st.button("Save URL")
if save_button and url:
    save_url(url)
    st.success("URL saved!")

# Display the uploaded files
uploaded_files = os.listdir(UPLOAD_DIRECTORY)
st.subheader("Uploaded Files")
for file_name in uploaded_files:
    st.write(file_name)
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    if file_name.endswith((".pdf", ".doc")):
        download_file(file_path, file_name)
    elif file_name.endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(file_path)
        st.image(image)
        download_file(file_path, file_name)

# Display the saved URLs
st.subheader("Saved URLs")
c.execute("SELECT * FROM urls")
urls = c.fetchall()
for url in urls:
    st.write(url[0])

# Close the database connection
conn.close()

st.write("---")
st.markdown("Copyright © 2023 [Edu](#) . All Rights Reserved.")
st.write("Rabi ynajhna kol, amin ya rabi :open_hands:")
st.write("Jasser ")
st.write("Bac 2024 admis")
