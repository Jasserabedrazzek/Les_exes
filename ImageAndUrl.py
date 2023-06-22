import streamlit as st
import os
import base64

# Create a folder for storing uploaded images if it doesn't exist
UPLOAD_FOLDER = "uploaded_images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set Streamlit page configuration
st.set_page_config(
    page_title="4eme secondaire image and url",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Page title
st.title('Bac 2024 doc')

# Upload image function
def upload_image():
    uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded image to the upload folder
            image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Display the uploaded image
            st.image(image_path, caption=uploaded_file.name, use_column_width=True)
            
            # Create a download link for the uploaded image
            download_link = get_download_link(image_path, uploaded_file.name)
            st.markdown(download_link, unsafe_allow_html=True)

# Generate a download link for a file
def get_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        file_data = f.read()
    encoded_file = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{encoded_file}" download="{file_name}">Download {file_name}</a>'
    return href

# Show uploaded images from the upload folder
uploaded_images = os.listdir(UPLOAD_FOLDER)
if uploaded_images:
    st.subheader("Uploaded Images")
    for image_name in uploaded_images:
        image_path = os.path.join(UPLOAD_FOLDER, image_name)
        st.image(image_path, caption=image_name, use_column_width=True)
        download_link = get_download_link(image_path, image_name)
        st.markdown(download_link, unsafe_allow_html=True)

# Upload images
upload_image()
