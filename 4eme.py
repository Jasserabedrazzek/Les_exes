import streamlit as st
import os
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('documents.db')
c = conn.cursor()

# Create a table to store the uploaded documents
c.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT
    )
''')

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire Pdf",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Display the page title
st.title('Bac 2024 doc')

# Upload file function
def upload_file():
    uploaded_file = st.file_uploader("Upload PDF or DOC file", type=["pdf", "docx"], accept_multiple_files=True)
    if uploaded_file is not None:
        for file in uploaded_file:
            filename = file.name
            save_uploaded_file(file, filename)
            # Save the filename to the database
            c.execute("INSERT INTO documents (filename) VALUES (?)", (filename,))
            conn.commit()
        st.success("File(s) uploaded successfully!")

# Save the uploaded file to a folder
def save_uploaded_file(uploaded_file, filename):
    with open(os.path.join("uploads", filename), "wb") as f:
        f.write(uploaded_file.getbuffer())

# Display the uploaded documents
def display_documents():
    c.execute("SELECT * FROM documents")
    documents = c.fetchall()
    if documents:
        st.subheader("Uploaded Documents:")
        for doc in documents:
            st.write(doc[1])

# Download file function
def download_file(filename):
    st.markdown(f'<a href="uploads/{filename}" download="{filename}">Download {filename}</a>', unsafe_allow_html=True)

# Display the uploaded documents and download buttons
display_documents()
if st.button("Refresh"):
    display_documents()

# Display the upload file section
st.subheader("Upload File(s):")
upload_file()

# Download file section
st.subheader("Download File(s):")
c.execute("SELECT * FROM documents")
documents = c.fetchall()
for doc in documents:
    download_file(doc[1])

# Close the database connection
conn.close()
