import streamlit as st
import requests

# Define the URL of your Flask server
FLASK_URL = 'http://localhost:5000/process'  # Update with your Flask server's URL

# Function to send a request to Flask server
def process_images(uploaded_files):
    # Create a dictionary to hold the uploaded files
    files = [('images', (file.name, file.read(), file.type)) for file in uploaded_files]

    # Send POST request with the files
    response = requests.post(FLASK_URL, files=files)
    
    if response.status_code == 200:
        return response.text
    else:
        return f'Error: {response.status_code} - {response.text}'

# Streamlit app
def main():
    st.title('Traffic Tracker')
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    # Button to trigger image processing
    if st.button('Process Images'):
        if uploaded_files:
            st.write('Processing images...')
            result = process_images(uploaded_files)
            st.write('Result:')
            st.write(result)
            
        else:
            st.write('Please upload images first.')

if __name__ == '__main__':
    main()
