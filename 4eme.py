import streamlit as st
import sqlite3

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

# Download file
def download_file(filename):
    st.markdown(f'<a href="file_uploads/{filename}" download>Click here to download</a>', unsafe_allow_html=True)

# Sidebar buttons for file upload
uploaded_file = st.sidebar.file_uploader("Upload PDF or DOC file", type=['pdf', 'doc'])
if uploaded_file is not None:
    upload_file(uploaded_file, uploaded_file.type.split('/')[-1])

uploaded_image = st.sidebar.file_uploader("Upload Image file", type=['png', 'jpg', 'jpeg'])
if uploaded_image is not None:
    upload_file(uploaded_image, 'image')

# Display uploaded files
display_files()
