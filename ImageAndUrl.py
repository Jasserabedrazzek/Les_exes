import streamlit as st
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('image_urls.db')
cursor = conn.cursor()

# Create a table to store image URLs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL
    )
''')
conn.commit()

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire image and url",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Display the app title
st.title('Bac 2024 doc')

# Create a file uploader for images
uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

# Loop over uploaded images and save them to the database
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        cursor.execute('INSERT INTO images (url) VALUES (?)', (file_bytes,))
        conn.commit()

# Create an input field for URLs
url = st.text_input("Enter URL")

# Save the URL to the database if provided
if url:
    cursor.execute('INSERT INTO images (url) VALUES (?)', (url,))
    conn.commit()

# Retrieve and display the uploaded images and URLs from the database
cursor.execute('SELECT * FROM images')
results = cursor.fetchall()

for result in results:
    if result[1].startswith('http'):
        st.markdown(f"URL: [{result[1]}]({result[1]})")
    else:
        st.image(result[1])

# Create a button to download the images
if st.button("Download Images"):
    for result in results:
        if not result[1].startswith('http'):
            img_data = result[1]
            st.download_button(f"Download Image {result[0]}", img_data, file_name=f"image{result[0]}")

# Close the database connection
cursor.close()
conn.close()
