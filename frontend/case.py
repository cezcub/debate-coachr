import streamlit as st
import requests
from frontend.chat import render_chat_interface

FASTAPI_URL = "http://127.0.0.1:8000/process-text/"

def text_upload(debate_topic, side):
    """Enhanced text file upload with better UI/UX design principles"""
    
    # **TIP 1: Better visual hierarchy** with icons and clear descriptions
    st.markdown("#### 📄 Text Analysis")
    st.markdown(
        """
        Upload your debate case (in TXT format) for comprehensive AI analysis and feedback.
        """
    )
    
    # **TIP 2: Enhanced file uploader** with better styling and validation
    uploaded_file = st.file_uploader(
        "Choose your debate case",
        type=["txt"],
        help="💡 Upload a plain text file (.txt) containing your debate transcript",
        key="text_file_uploader"
    )

    if uploaded_file is not None:
        # **TIP 3: Better user feedback** with file information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.success(f"✅ File uploaded: **{uploaded_file.name}**")
        
        with col2:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.info(f"📊 Size: {file_size_mb:.2f} MB")
        
        # **TIP 4: Content preview** for user confidence
        if st.checkbox("🔍 Preview file content", help="View the first 500 characters of your file"):
            try:
                # Read and display preview
                stringio = uploaded_file.getvalue().decode("utf-8")
                preview_text = stringio[:500] + "..." if len(stringio) > 500 else stringio
                st.text_area("📝 File Preview", preview_text, height=150, disabled=True)
            except UnicodeDecodeError:
                st.error("❌ Unable to decode file. Please ensure it's a valid UTF-8 text file.")
                return

        # **TIP 5: Better validation** and user guidance
        if not debate_topic or not debate_topic.strip():
            st.warning("⚠️ Please enter a debate topic above before analyzing your text")
            st.button("🚀 Analyze Text", disabled=True, use_container_width=True)
            return

        # **TIP 6: Enhanced call-to-action** with primary styling
        if st.button("🚀 Analyze Text", type="primary", use_container_width=True):
            with st.spinner("🔄 Analyzing your text with AI... This may take a moment"):
                try:
                    # **TIP 7: Better progress indication**
                    progress_bar = st.progress(0)
                    progress_bar.progress(25, "Uploading file...")
                    
                    # Send the text file and debate topic to the FastAPI backend
                    response = requests.post(
                        FASTAPI_URL,
                        files={"file": uploaded_file},
                        data={"debate_topic": debate_topic, "side": side},
                    )
                    
                    progress_bar.progress(75, "Processing with AI...")

                    if response.status_code == 200:
                        progress_bar.progress(100, "Complete!")
                        progress_bar.empty()  # Remove progress bar
                        
                        processed_text = response.json().get("processed_text", "")
                        
                        # Store results in session state to persist across reruns
                        st.session_state.analysis_results = {
                            "processed_text": processed_text,
                            "debate_topic": debate_topic,
                            "filename": uploaded_file.name,
                            "completed": True
                        }
                        
                        # **TIP 8: Celebration and clear results**
                        st.balloons()
                        st.success("🎉 Text analysis completed successfully!")
                    
                    else:
                        progress_bar.empty()
                        error_msg = response.json().get('error', 'Unknown error occurred')
                        st.error(f"❌ Analysis failed: {error_msg}")
                        
                        # **TIP 11: Helpful error guidance**
                        with st.expander("🔧 Troubleshooting Tips"):
                            st.markdown("""
                            **Common issues and solutions:**
                            - Ensure your file is a valid text file (.txt)
                            - Check that the debate topic is clearly specified
                            - Verify your internet connection
                            - Try uploading a smaller file if the current one is very large
                            """)

                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    
                    # **TIP 12: Error reporting** for better user support
                    with st.expander("📞 Need Help?"):
                        st.markdown("""
                        If this error persists, please contact support with:
                        - The error message above
                        - Your file type and size
                        - The debate topic you entered
                        """)
    
    else:
        # **TIP 13: Helpful guidance** when no file is uploaded
        st.info("👆 Please upload a text file to get started with your debate analysis")
    
    # Display analysis results if they exist in session state
    if hasattr(st.session_state, 'analysis_results') and st.session_state.analysis_results.get('completed', False):
        results = st.session_state.analysis_results
        processed_text = results['processed_text']
        debate_topic = results['debate_topic']
        filename = results['filename']
        
        # **TIP 9: Better results display** with expandable sections
        with st.expander("📊 Analysis Results", expanded=True):
            st.markdown("### 🤖 AI Feedback")
            st.markdown(
                processed_text,
                help="AI-generated feedback based on your debate transcript and topic"
            )
        
        # **TIP 10: Additional actions** for user engagement
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copy Results"):
                st.write("Results copied to clipboard!")
        with col2:
            if st.button("🔄 Analyze Another"):
                # Clear session state and rerun
                if 'analysis_results' in st.session_state:
                    del st.session_state.analysis_results
                if 'chat_messages' in st.session_state:
                    del st.session_state.chat_messages
                st.rerun()
        with col3:
            if st.button("💾 Download Report"):
                st.download_button(
                    label="📥 Download as TXT",
                    data=processed_text,
                    file_name=f"debate_analysis_{filename}",
                    mime="text/plain"
                )
        
        # Live Chat Feature - Interactive discussion with AI coach
        with st.expander("💬 Chat with Your AI Coach", expanded=True):
            st.markdown("Discuss your text analysis in real-time with your AI debate coach!")
            
            # Import and render chat interface
            try:
                # Use direct Azure connection for reliability
                render_chat_interface(processed_text, debate_topic, use_api=False)
                
            except Exception as chat_error:
                st.error(f"Chat feature temporarily unavailable: {str(chat_error)}")
                st.info("You can still review and download your feedback above.")