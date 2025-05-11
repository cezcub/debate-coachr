import streamlit as st
import requests
import os

def get_feedback(temp_audio_path, url, resolution):
    with st.spinner("Analyzing round (this may take a few minutes)..."):
        try:
            # Send the audio file to the FastAPI backend
            with open(temp_audio_path, "rb") as audio_file:
                response = requests.post(url, files={"file": audio_file}, data={"resolution": resolution})

            # Handle the response
            if response.status_code == 200:
                response_data = response.json()
                azure_output = response_data.get("azure_output", "")

                st.success("Processing completed!")
                st.text_area("Azure Output", azure_output, height=200)
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Clean up the temporary file after use
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)