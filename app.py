import streamlit as st
from frontend.pf_feedback import get_feedback
from frontend.case import text_upload

FASTAPI_URL = "http://127.0.0.1:8000/"

def main():
    # **TIP 1: Page Configuration** - Set proper page config with wide layout and custom theme
    st.set_page_config(
        page_title="Coachr - AI Debate Coach",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# Coachr AI\nYour intelligent debate coaching assistant powered by Azure OpenAI!"
        }
    )

    # **TIP 2: Custom CSS** for better aesthetics
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # **TIP 3: Hero Section with Better Typography**
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Coachr - AI Debate Coach</h1>
        <p style="font-size: 1.2em; margin-bottom: 0;">Transform your debate skills with intelligent AI feedback</p>
    </div>
    """, unsafe_allow_html=True)

    # **TIP 4: Column Layout** for better organization
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # **TIP 5: Enhanced Sidebar** with better organization
        st.markdown("### 🚀 Get Started")
        
        # Feature selection with better UI
        option = st.selectbox(
            "Choose your analysis type:",
            ["🎙️ Audio Analysis", "📄 Text Analysis"],
            help="Select whether you want to analyze an audio recording or text transcript"
        )
        
        st.markdown("---")
        
        # **TIP 6: Information hierarchy** with expanders
        with st.expander("📚 How to Use", expanded=False):
            st.markdown("""
            **For Audio Analysis:**
            1. Enter your debate topic
            2. Upload your audio file
            3. Click 'Get AI Feedback'
            
            **For Text Analysis:**
            1. Enter your debate topic  
            2. Upload your text file
            3. Click 'Analyze Text'
            """)
        
        with st.expander("🎯 Supported Formats", expanded=False):
            st.markdown("""
            **Audio Files:**
            - MP3, WAV, OGG, FLAC, M4A
            
            **Text Files:**
            - TXT files only
            """)
        
        with st.expander("💡 Tips for Better Results", expanded=False):
            st.markdown("""
            - Use clear, high-quality audio
            - Provide specific debate topics
            - Upload complete rounds when possible
            - Check file size limits
            """)

    with col2:
        # **TIP 7: Better form organization** with containers
        with st.container():
            st.markdown("### 📝 Debate Details")
            
            # Enhanced topic input with better placeholder
            debate_topic = st.text_input(
                "🎭 Debate Topic/Resolution",
                placeholder="e.g., This house believes that artificial intelligence should be regulated",
                help="📌 Be specific! Include the exact resolution or topic for more targeted feedback.",
                key="debate_topic"
            )
        
        # **TIP 8: Better visual separation** and status indicators
        if option == "🎙️ Audio Analysis":
            st.markdown("### 🎙️ Audio File Upload")
            
            # Custom upload area styling
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Choose an audio file",
                type=["mp3", "wav", "ogg", "flac", "m4a"],
                help="💡 Tip: Higher quality audio produces better transcription results"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if uploaded_file is not None:
                # **TIP 9: Progress indicators** and user feedback
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # File details in an info box
                file_details = {"filename": uploaded_file.name, "filesize": uploaded_file.size}
                st.info(f"📊 File size: {file_details['filesize']:,} bytes")
                
                # Save the uploaded file temporarily
                with open("temp_uploaded_audio.wav", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                temp_audio_path = "temp_uploaded_audio.wav"

                # **TIP 10: Interactive preview** - Display the uploaded audio file
                st.markdown("#### 🔊 Audio Preview")
                st.audio(temp_audio_path, format="audio/wav")

                # **TIP 11: Better call-to-action** buttons with validation
                if debate_topic.strip():  # Only enable if topic is provided
                    if st.button("🚀 Get AI Feedback", type="primary", use_container_width=True):
                        with st.spinner("🔄 Processing your audio and generating feedback..."):
                            try:
                                get_feedback(temp_audio_path, FASTAPI_URL + "transcribe/", debate_topic)
                                st.balloons()  # Celebration animation
                                st.success("🎉 Analysis complete! Your feedback is ready below.")
                            except Exception as e:
                                st.error(f"❌ An error occurred: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a debate topic before proceeding")
                    st.button("🚀 Get AI Feedback", disabled=True, use_container_width=True)

        elif option == "📄 Text Analysis":
            st.markdown("### 📄 Text File Upload")
            
            # **TIP 12: Consistent styling** across different sections
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.markdown("Upload your debate transcript for AI-powered analysis and feedback.")
            text_upload(debate_topic)
            st.markdown('</div>', unsafe_allow_html=True)

    # **TIP 13: Footer with additional information** and branding
    st.markdown("---")
    
    # Statistics or status area
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("🎯 Analysis Types", "2", delta="Audio & Text")
    
    with col_stat2:
        st.metric("🤖 AI Model", "GPT-4", delta="Azure OpenAI")
    
    with col_stat3:
        st.metric("⚡ Response Time", "< 2 min", delta="Average")

    # **TIP 14: About section** with better information hierarchy
    with st.expander("ℹ️ About Coachr", expanded=False):
        st.markdown("""
        **Coachr** is an AI-powered debate coaching platform that provides:
        
        - 🎯 **Intelligent Analysis**: Advanced AI feedback on your debate performance
        - 📊 **Detailed Insights**: Comprehensive breakdown of arguments and delivery
        - 🚀 **Instant Results**: Get feedback in minutes, not hours
        - 🔒 **Secure Processing**: Your data is processed securely and privately
        
        Powered by **Azure OpenAI** and **Whisper** for best-in-class accuracy.
        """)

if __name__ == "__main__":
    main()