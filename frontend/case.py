import streamlit as st
import requests
from frontend.chat import render_chat_interface

FASTAPI_URL = "http://127.0.0.1:8000/process-text/"

def text_upload(debate_topic, side):
    """Enhanced text file upload with better UI/UX design principles"""
    
    # **TIP 1: Better visual hierarchy** with icons and clear descriptions
    st.markdown("#### 📄 Case Analysis")
    st.markdown(
        """
        Upload your debate case for comprehensive AI analysis and feedback. 
        Supports TXT files for plaintext cases and DOCX/PDF files for structured card format with bold/highlighted text extraction.
        """
    )
    
    # **NEW: Upload format selection**
    st.markdown("##### 📋 Upload Format")
    upload_format = st.radio(
        "Select your case format:",
        ["plaintext", "card format"],
        help="Choose 'plaintext' for regular text files or 'card format' for structured debate cards",
        horizontal=True,
        key="upload_format_selector"
    )
    
    # Display format-specific information and determine allowed file types
    if upload_format == "plaintext":
        st.info("📝 **Plaintext Format**: Upload any text file containing your debate case or arguments.")
        allowed_types = ["txt"]
        help_text = "💡 Upload a plain text file (.txt) containing your plaintext debate content"
    else:
        st.info("🃏 **Card Format**: Upload structured debate cards with evidence, tags, and citations.")
        st.warning("⚠️ DOCX files are preferred and work better and faster. Card format processing extracts bolded and highlighted text from DOCX/PDF files.")
        allowed_types = ["docx", "pdf", "txt"]
        help_text = "💡 Upload a DOCX, PDF, or TXT file containing your card format debate content"
    
    # **TIP 2: Enhanced file uploader** with better styling and validation
    uploaded_file = st.file_uploader(
        f"Choose your debate case ({upload_format})",
        type=allowed_types,
        help=help_text,
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
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if st.checkbox("🔍 Preview file content", help="View the first 500 characters of your file"):
            try:
                if file_extension == "txt":
                    # Read and display preview for text files
                    stringio = uploaded_file.getvalue().decode("utf-8")
                    preview_text = stringio[:500] + "..." if len(stringio) > 500 else stringio
                    st.text_area("📝 File Preview", preview_text, height=150, disabled=True)
                elif file_extension in ["docx", "pdf"]:
                    # Show file info for binary files
                    st.info(f"📄 {file_extension.upper()} file detected. Preview will show extracted text after processing.")
                    st.text_area("📝 File Info", f"File: {uploaded_file.name}\nType: {file_extension.upper()}\nSize: {uploaded_file.size} bytes", height=100, disabled=True)
                else:
                    st.warning("⚠️ Unsupported file type for preview.")
            except UnicodeDecodeError:
                st.error("❌ Unable to decode file. Please ensure it's a valid file.")
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
                    
                    # Update progress message based on file type
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    if file_extension in ["docx", "pdf"] and upload_format == "card format":
                        progress_bar.progress(25, "Extracting formatted text from document...")
                    else:
                        progress_bar.progress(25, "Uploading file...")
                    
                    # Send the file, debate topic, and upload format to the FastAPI backend
                    current_upload_format = upload_format  # Direct variable
                    
                    response = requests.post(
                        FASTAPI_URL,
                        files={"file": uploaded_file},
                        data={
                            "debate_topic": debate_topic, 
                            "side": side,
                            "upload_format": current_upload_format,
                            "file_extension": file_extension
                        },
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
                            "upload_format": current_upload_format,
                            "completed": True
                        }
                        
                        # **TIP 8: Clear results**
                        st.success("🎉 Text analysis completed successfully!")
                    
                    else:
                        progress_bar.empty()
                        error_msg = response.json().get('error', 'Unknown error occurred')
                        
                        # Enhanced error handling for document processing
                        if "File processing error" in error_msg:
                            st.error(f"❌ Document Processing Failed: {error_msg}")
                            with st.expander("📋 Document Processing Tips"):
                                st.markdown("""
                                **For DOCX files:**
                                - Ensure the file is a valid Microsoft Word document
                                - Check that the file contains bolded or highlighted text for card format
                                - Try saving the file in a newer DOCX format
                                
                                **For PDF files:**
                                - Ensure the PDF contains selectable text (not scanned images)
                                - PDF formatting detection has limitations - consider using DOCX for better results
                                - For card format, ensure text is clearly formatted
                                """)
                        else:
                            st.error(f"❌ Analysis failed: {error_msg}")
                        
                        # **TIP 11: Helpful error guidance**
                        with st.expander("🔧 General Troubleshooting Tips"):
                            st.markdown("""
                            **Common issues and solutions:**
                            - Ensure your file is in a supported format (TXT, DOCX, PDF)
                            - Check that the debate topic is clearly specified
                            - Verify your internet connection
                            - Try uploading a smaller file if the current one is very large
                            - For card format, ensure your document has proper formatting (bold/highlight)
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
        format_specific_help = {
            "plaintext": "👆 Please upload a text file (.txt) to get started with your debate analysis",
            "card format": "👆 Please upload a document file (.txt, .docx, .pdf) containing your debate cards. For best results with card format, use DOCX files with bolded or highlighted text."
        }
        st.info(format_specific_help.get(upload_format, "👆 Please upload a file to get started"))
    
    # Display analysis results if they exist in session state
    if hasattr(st.session_state, 'analysis_results') and st.session_state.analysis_results.get('completed', False):
        results = st.session_state.analysis_results
        processed_text = results['processed_text']
        debate_topic = results['debate_topic']
        filename = results['filename']
        upload_format = results.get('upload_format', 'plaintext')  # Default to plaintext for backward compatibility
        
        # **TIP 9: Better results display** with expandable sections
        with st.expander("📊 Analysis Results", expanded=True):
            # Show upload format information
            format_icon = "📝" if upload_format == "plaintext" else "🃏"
            st.markdown(f"**Format:** {format_icon} {upload_format.title()}")
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