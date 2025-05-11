import streamlit as st
from f_pf_feedback import get_feedback
from f_case import text_upload

FASTAPI_URL = "http://127.0.0.1:8000/"

def main():
    # Set the page configuration
    st.set_page_config(
        page_title="Outreach Debate - AI Feedback",
        page_icon="🎙️",
        layout="centered",
    )

    # Add a header with a title and description
    st.title("🎙️ Debate Coaching")
    st.markdown(
        """
        Welcome to **Coachr**!  
        Upload your round, and we'll give you feedback and analysis.  
        """
    )

    # Add a sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        option = st.radio("Choose a feature:", ["Audio Feedback", "Text File Processing"])

    # Add a text input for the debate topic
    debate_topic = st.text_input(
        "Enter the Debate Topic",
        placeholder="E.g., Should AI be regulated?",
        help="Provide the topic of the debate for better feedback and analysis.",
    )

    if option == "Audio Feedback":
        # File uploader for audio files
        st.subheader("Upload Your Audio File")
        uploaded_file = st.file_uploader(
            "Choose an audio file", type=["mp3", "wav", "ogg", "flac", "m4a"]
        )

        if uploaded_file is not None:
            # Save the uploaded file temporarily
            with open("temp_uploaded_audio.wav", "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_audio_path = "temp_uploaded_audio.wav"

            # Display the uploaded audio file
            st.audio(temp_audio_path, format="audio/wav")
            st.success("Audio file uploaded successfully!")

            # Transcription button
            if st.button("🔍 Get Feedback"):
                with st.spinner("Processing..."):
                    get_feedback(temp_audio_path, FASTAPI_URL + "transcribe/", debate_topic)
                    st.success("Feedback received! Check the results below.")

    elif option == "Text File Processing":
        text_upload(debate_topic)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        **Developed by OutreachAI**  
        Powered by [Streamlit](https://streamlit.io/) and Azure OpenAI.
        """
    )

if __name__ == "__main__":
    main()