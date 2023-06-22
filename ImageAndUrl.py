import streamlit as st
import sqlite3
from PIL import Image
import requests
from io import BytesIO

# Create a connection to the SQLite database
conn = sqlite3.connect('image_urls.db')
cursor = conn.cursor()

# Create a table to store image URLs
cursor.execute('''CREATE TABLE IF NOT EXISTS images
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  image BLOB,
                  url TEXT)''')
conn.commit()

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire image and url",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Display title
st.title('Bac 2024 doc')

# Create a button to upload an image
uploaded_file = st.file_uploader("Upload an image")

# Create an input field to enter a URL (optional)
url = st.text_input("Enter a URL (optional)")

# Save the uploaded image or URL to the database
if uploaded_file or url:
    if uploaded_file:
        image = uploaded_file.read()
        cursor.execute("INSERT INTO images (image) VALUES (?)", (image,))
    if url:
        cursor.execute("INSERT INTO images (url) VALUES (?)", (url,))
    conn.commit()

# Retrieve and display all stored images or URLs from the database
cursor.execute("SELECT * FROM images")
results = cursor.fetchall()
for result in results:
    image_id, image_blob, image_url = result
    if image_blob:
        st.image(image_blob, caption="Uploaded Image")
    elif image_url:
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                pil_image = Image.open(BytesIO(response.content))
                st.image(pil_image, caption="URL Image")

                # Create a button to download the image
                file_name = f"image_{image_id}.png"
                st.download_button("Download Image", data=response.content, file_name=file_name)
        except Exception as e:
            st.error(f"Error loading image from URL: {e}")

# Close the database connection
cursor.close()
conn.close()
