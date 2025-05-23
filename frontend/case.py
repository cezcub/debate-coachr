import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000/process-text/"

def text_upload(resolution):
    st.title("📄 Text File Processing")
    st.markdown(
        """
        Upload a text file, and we'll process it for you.  
        """
    )

    # File uploader for text files
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file is not None:
        # Display the uploaded file name
        st.success(f"Uploaded file: {uploaded_file.name}")

        # Process the text file
        if st.button("🔍 Process Text"):
            with st.spinner("Processing..."):
                try:
                    # Send the text file and debate topic to the FastAPI backend
                    response = requests.post(
                        FASTAPI_URL,
                        files={"file": uploaded_file},
                        data={"resolution": resolution},
                    )

                    if response.status_code == 200:
                        processed_text = response.json().get("processed_text", "")
                        st.success("Text processed successfully!")
                        st.text_area("Processed Text", processed_text, height=300)
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")