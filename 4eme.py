import streamlit as st
import sqlite3
import uuid

# Create a SQLite database connection
conn = sqlite3.connect('file_uploads.db')
c = conn.cursor()

# Create a table to store file uploads
c.execute('''CREATE TABLE IF NOT EXISTS uploads
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              filename TEXT,
              filetype TEXT)''')
conn.commit()

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire Pdf",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title('Bac 2024 doc')

# File upload and database insertion functions
def upload_file(file, filetype):
    with open(file.name, 'wb') as f:
        f.write(file.getbuffer())
    c.execute("INSERT INTO uploads (filename, filetype) VALUES (?, ?)", (file.name, filetype))
    conn.commit()

# Display uploaded files and provide download buttons
def display_files():
    c.execute("SELECT filename, filetype FROM uploads")
    files = c.fetchall()
    for file in files:
        st.write(file[0])
        if file[1] in ('pdf', 'doc'):
            st.button('Download', key=file[0], on_click=download_file, args=(file[0],))
        elif file[1] == 'image':
            st.image(file[0])
            unique_key = str(uuid.uuid4())
            st.button('Download', key=f'download_{file[0]}_{unique_key}', on_click=download_file, args=(file[0],))

# Download file
def download_file(filename):
    st.markdown(f'<a href="file_uploads/{filename}" download>Click here to download</a>', unsafe_allow_html=True)

# Sidebar buttons for file upload
uploaded_files = st.sidebar.file_uploader("Upload PDF or DOC files", accept_multiple_files=True, type=['pdf', 'doc'])
if uploaded_files is not None:
    for file in uploaded_files:
        upload_file(file, file.type.split('/')[-1])

uploaded_images = st.sidebar.file_uploader("Upload Image files", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
if uploaded_images is not None:
    for image in uploaded_images:
        upload_file(image, 'image')

# Display uploaded files
display_files()
