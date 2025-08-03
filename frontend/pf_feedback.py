import streamlit as st
import requests
import os
import time
from frontend.chat import render_chat_interface

def get_feedback(temp_audio_path, url, debate_topic, side):
    """Enhanced audio feedback function with better UI/UX design principles"""
    
    # **TIP 1: Better progress indication** with detailed steps
    progress_container = st.container()
    status_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Processing Your Audio")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # **TIP 2: Step-by-step progress** for better user experience
        with status_container:
            status_text.text("🎯 Initializing analysis...")
            progress_bar.progress(10)
            time.sleep(0.5)  # Brief pause for better UX
            
            status_text.text("📤 Uploading audio file...")
            progress_bar.progress(25)
            
            # Send the audio file to the FastAPI backend
            with open(temp_audio_path, "rb") as audio_file:
                response = requests.post(
                    url, 
                    files={"file": audio_file}, 
                    data={"debate_topic": debate_topic, "side": side}
                )
            
            status_text.text("🎙️ Transcribing audio...")
            progress_bar.progress(50)
            
            status_text.text("🤖 Generating AI feedback...")
            progress_bar.progress(75)

            # Handle the response
            if response.status_code == 200:
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                response_data = response.json()
                azure_output = response_data.get("azure_output", "")
                
                # Store results in session state to persist across reruns
                st.session_state.pf_analysis_results = {
                    "azure_output": azure_output,
                    "debate_topic": debate_topic,
                    "side": side,
                    "audio_path": temp_audio_path,
                    "completed": True
                }
                
                # **TIP 3: Success feedback**
                st.success("🎉 Your debate analysis is ready!")
            
            else:
                progress_bar.empty()
                status_text.empty()
                
                error_msg = response.json().get('error', 'Unknown error occurred')
                st.error(f"❌ Analysis failed: {error_msg}")
                
                # **TIP 12: Enhanced error guidance** for Azure connection issues
                with st.expander("🔧 Troubleshooting"):
                    if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                        st.markdown("""
                        **Azure Authentication Issue:**
                        
                        - ❌ The AI service authentication failed
                        - 🔑 This usually means the API key is invalid or missing
                        - 👨‍💻 Please contact the administrator to check Azure OpenAI credentials
                        """)
                    elif "connection" in error_msg.lower() or "endpoint" in error_msg.lower():
                        st.markdown("""
                        **Connection Issue:**
                        
                        - 🌐 Cannot connect to Azure OpenAI service
                        - 📡 This could be a network or configuration issue
                        - 🔗 Please check the Azure endpoint configuration
                        """)
                    else:
                        st.markdown("""
                        **Common issues and solutions:**
                        
                        - **Audio Quality**: Ensure your audio is clear and not too quiet
                        - **File Format**: Try converting to MP3 or WAV format
                        - **File Size**: Large files may take longer or fail to process
                        - **Network**: Check your internet connection
                        - **Topic**: Ensure you've entered a clear debate topic
                        - **AI Service**: The AI analysis service may be temporarily unavailable
                        """)
                
                # **TIP 13: Support contact**
                st.info("💬 If the problem persists, please contact support with the error details above.")

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        
        # **TIP 14: Detailed error reporting**
        with st.expander("📞 Error Details"):
            st.code(f"Error Type: {type(e).__name__}\nError Message: {str(e)}")
            st.markdown("""
            **What you can try:**
            1. Refresh the page and try again
            2. Check your audio file format and size
            3. Verify your internet connection
            4. Contact support if the issue persists
            """)

    finally:
        # **TIP 15: Clean resource management**
        try:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
        except Exception as cleanup_error:
            st.sidebar.warning(f"⚠️ Cleanup warning: {cleanup_error}")

def get_audio_duration(audio_path):
    """Get audio duration in seconds (simplified version)"""
    try:
        # This is a simplified duration calculation
        # In a real implementation, you might use librosa or pydub
        import os
        file_size = os.path.getsize(audio_path)
        # Rough estimate: 1MB ≈ 60 seconds for compressed audio
        estimated_duration = (file_size / 1024 / 1024) * 60
        return min(estimated_duration, 600)  # Cap at 10 minutes for display
    except:
        return 0.0

def display_pf_results():
    """Display persistent feedback results from session state"""
    # Display analysis results if they exist in session state
    if hasattr(st.session_state, 'pf_analysis_results') and st.session_state.pf_analysis_results.get('completed', False):
        results = st.session_state.pf_analysis_results
        azure_output = results['azure_output']
        debate_topic = results['debate_topic']
        side = results['side']
        audio_path = results.get('audio_path', '')
        
        # **TIP 4: Enhanced results display** with better organization
        st.markdown("---")
        
        # **TIP 5: Tabbed interface** for better content organization
        tab1, tab2, tab3 = st.tabs(["📊 AI Feedback", "📝 Tips & Insights", "🎯 Action Items"])
        
        with tab1:
            st.markdown("### 🤖 Comprehensive AI Analysis")
            st.markdown(f"**Debate Topic:** {debate_topic}")
            st.markdown(f"**Side:** {side}")
            st.markdown("---")
            
            # **TIP 6: Better text display** with formatting
            if azure_output:
                st.markdown(
                    azure_output,
                    help="AI-generated analysis of your debate performance"
                )
                
                # **TIP 7: Additional actions** for user engagement
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 Copy Feedback", use_container_width=True):
                        st.write("Feedback copied to clipboard!")
                
                with col2:
                    st.download_button(
                        label="💾 Download Report",
                        data=azure_output,
                        file_name=f"debate_feedback_{int(time.time())}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col3:
                    if st.button("🔄 Analyze Another", use_container_width=True):
                        # Clear session state and rerun
                        if 'pf_analysis_results' in st.session_state:
                            del st.session_state.pf_analysis_results
                        if 'chat_messages' in st.session_state:
                            del st.session_state.chat_messages
                        st.rerun()
            
            else:
                st.warning("⚠️ No feedback content received from the AI service.")
        
        with tab2:
            st.markdown("### 💡 Performance Insights")
            
            # **TIP 8: Visual metrics** for engagement
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🎯 Analysis Type", "Audio", delta="Real-time")
            
            with col2:
                if audio_path and os.path.exists(audio_path):
                    audio_duration = get_audio_duration(audio_path)
                    st.metric("⏱️ Audio Length", f"{audio_duration:.1f}s", delta="Processed")
                else:
                    st.metric("⏱️ Audio Length", "N/A", delta="Processed")
            
            with col3:
                feedback_length = len(azure_output.split()) if azure_output else 0
                st.metric("📝 Feedback Words", str(feedback_length), delta="Generated")
            
            # **TIP 9: Helpful tips** based on analysis
            st.markdown("#### 🎯 Quick Tips for Improvement")
            st.info("""
            **Based on your analysis:**
            - 🗣️ Focus on clear articulation and pacing
            - 📊 Structure your arguments logically
            - 🎯 Address counterarguments effectively
            - ⏰ Manage your time efficiently
            """)
        
        with tab3:
            st.markdown("### 🎯 Next Steps")
            
            # **TIP 10: Actionable recommendations**
            st.markdown("""
            **Recommended Actions:**
            
            1. **📝 Review the feedback** - Read through all AI suggestions carefully
            2. **🎯 Identify key areas** - Focus on 2-3 main improvement points
            3. **🎭 Practice specific skills** - Work on the highlighted areas
            4. **🔄 Record again** - Upload another round to track progress
            5. **📚 Study examples** - Research effective debate techniques
            """)
            
            # **TIP 11: Progress tracking**
            st.markdown("#### 📈 Track Your Progress")
            if st.button("📊 View Progress Dashboard", use_container_width=True):
                st.info("Progress tracking feature coming soon!")
        
        # **Live Chat Feature** - Interactive discussion with AI coach
        with st.expander("💬 Chat with Your AI Coach", expanded=True):
            st.markdown("Discuss your feedback in real-time with your AI debate coach!")
            
            # Import and render chat interface
            try:
                # Use direct Azure connection for reliability
                render_chat_interface(azure_output, debate_topic, use_api=False)
                
            except Exception as chat_error:
                st.error(f"Chat feature temporarily unavailable: {str(chat_error)}")
                st.info("You can still review and download your feedback above.")