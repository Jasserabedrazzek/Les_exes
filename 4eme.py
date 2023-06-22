import streamlit as st
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('uploaded_files.db')
c = conn.cursor()

# Create the 'files' table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS files
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              file BLOB,
              file_type TEXT)''')
conn.commit()

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire Pdf",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Function to insert file into the database
def insert_file(file, file_type):
    c.execute("INSERT INTO files (file, file_type) VALUES (?, ?)", (file, file_type))
    conn.commit()

# Function to retrieve all uploaded files from the database
def get_uploaded_files():
    c.execute("SELECT * FROM files")
    return c.fetchall()

# Streamlit web application
st.title('Bac 2024 doc')

# Upload PDF or DOC button
uploaded_file = st.file_uploader("Upload PDF or DOC file", type=["pdf", "docx"])
if uploaded_file is not None:
    file_type = uploaded_file.type.split('/')[1]
    insert_file(uploaded_file.read(), file_type)
    st.success('File uploaded successfully!')

# Upload image button
uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    file_type = uploaded_image.type.split('/')[1]
    insert_file(uploaded_image.read(), file_type)
    st.success('Image uploaded successfully!')

# Show uploaded files
uploaded_files = get_uploaded_files()
for file in uploaded_files:
    file_id, _, file_type = file
    if file_type in ["pdf", "docx"]:
        st.write(f"File ID: {file_id}")
        download_button = st.button("Download", key=f"download_{file_id}")
        if download_button:
            st.download_button(label="Download", data=file[1], file_name=f"file.{file_type}")
    elif file_type in ["png", "jpg", "jpeg"]:
        st.write(f"File ID: {file_id}")
        st.image(file[1], use_column_width=True)

# Close the database connection
conn.close()
