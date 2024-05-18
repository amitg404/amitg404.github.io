import streamlit as st
import requests

# Define the URL of your Flask server
FLASK_URL = 'http://localhost:5000/process'  # Update with your Flask server's URL

# Streamlit app
def main():
    st.title('Traffic Tracker')
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    
    # Button to trigger image processing
    if st.button('Process Images'):
        if uploaded_files:
            st.write('Processing images...')
            files = {f"file_{i}": file for i, file in enumerate(uploaded_files)}
            response = requests.post(FLASK_URL, files=files)
            if response.status_code == 200:
                result = response.text
                st.write('Result:')
                st.write(result)
            else:
                st.write(f'Error: {response.status_code} - {response.text}')
        else:
            st.write('Please upload images first.')

if __name__ == '__main__':
    main()
