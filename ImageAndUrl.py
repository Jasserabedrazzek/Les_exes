import streamlit as st
import sqlite3

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
st.header("Images")

# Create a button to upload an image
uploaded_file = st.file_uploader("Upload an image")
st.header("Liens")

# Create an input field to enter a URL (optional)
url = st.text_input("Enter a URL (optional)")
st.header("Images Uploaded")

# Save the uploaded image or URL to the database
if uploaded_file or url:
    if uploaded_file:
        image = uploaded_file.read()
        cursor.execute("INSERT INTO images (image) VALUES (?)", (image,))
    if url:
        cursor.execute("INSERT INTO images (url) VALUES (?)", (url,))
    conn.commit()

# Retrieve the stored images or URLs from the database
cursor.execute("SELECT * FROM images")
results = cursor.fetchall()

# Display the images in columns
if results:
    num_columns = 3  # Number of columns to display the images
    chunks = [results[i:i + num_columns] for i in range(0, len(results), num_columns)]
    
    for chunk in chunks:
        columns = st.columns(num_columns)
        for image_id, image_blob, image_url in chunk:
            if image_blob:
                columns[image_id % num_columns].image(image_blob, caption="Uploaded Image")
                columns[image_id % num_columns].download_button(
                    f"Download Image {image_id}", data=image_blob, file_name=f"image_{image_id}.png"
                )
            elif image_url:
                columns[image_id % num_columns].image(image_url, caption="URL Image")

# Close the database connection
cursor.close()
conn.close()
