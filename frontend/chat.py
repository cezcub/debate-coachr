import streamlit as st
import time
import requests
import sys
import os

# Add the parent directory to the path to ensure imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from backend.azure import call_ai
except ImportError:
    # Fallback import path
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from backend.azure import call_ai

CHAT_API_URL = "http://127.0.0.1:8000/chat/"

def clear_chat():
    """Clear the chat messages and reset session state"""
    st.session_state.chat_messages = []
    st.session_state.chat_context = ""
    st.session_state.chat_topic = ""
    st.success("🗑️ Chat cleared successfully!")
    
def ai_response(user_input, use_api=False):
    """Generate AI response without UI elements to avoid interference with reruns"""
    try:
        if use_api:
            # Try API first but fall back to direct if it fails
            assistant_response = generate_chat_response_api(
                user_input, 
                st.session_state.chat_context,
                st.session_state.chat_topic,
                st.session_state.chat_messages
            )
        else:
            # Use direct Azure connection (recommended)
            assistant_response = generate_chat_response_direct(
                user_input, 
                st.session_state.chat_context,
                st.session_state.chat_topic,
                st.session_state.chat_messages
            )
        return assistant_response
    
    except Exception as e:
        error_msg = str(e).lower()
        if any(word in error_msg for word in ["connection", "timeout", "refused", "azure", "api"]):
            # Store error in session state to display later
            st.session_state.chat_error = "🔄 AI Coach connection issues - using fallback responses"
        fallback_response = generate_fallback_response(
            user_input,
            st.session_state.chat_context,
            st.session_state.chat_topic
        )
        return "I encountered a technical issue, but here's some general guidance: " + fallback_response

def render_chat_interface(initial_context, debate_topic, use_api=False):
    """
    Render an interactive chat interface for discussing feedback with AI
    
    Args:
        initial_context (str): The initial feedback/analysis to provide context
        debate_topic (str): The debate topic for context
        use_api (bool): Whether to use the FastAPI backend or direct Azure calls
                       Default False since FastAPI backend may not be running
    """
    
    # **TIP 1: Chat UI Header** with clear purpose and styling
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <h3 style='color: white; margin: 0;'>💬 Chat with Your AI Coach</h3>
        <p style='color: white; margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Ask questions about your feedback, get clarification, or explore improvement strategies!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # **TIP 2: Initialize chat session state**
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Always update context and topic for the current analysis
    st.session_state.chat_context = initial_context
    st.session_state.chat_topic = debate_topic
    
    # **TIP 3: Chat container** with better styling
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        if st.session_state.chat_messages:
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="🎓"):
                        st.markdown(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(message["content"])
        else:
            # **TIP 4: Welcome message** to start conversation
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown("""
                👋 Hello! I'm your AI debate coach. I've just analyzed your performance and I'm here to help you improve!
                
                **You can ask me about:**
                - Specific feedback points you'd like clarification on
                - Strategies to improve weak areas
                - Practice exercises for skill development
                - Questions about debate techniques
                - How to prepare for future rounds
                
                What would you like to discuss first?
                """)
    
    # **TIP 5: Chat input** with enhanced UX
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.chat_input(
            "Ask me anything about your debate performance...",
            key="chat_input"
        )
    
    with col2:
        clear_chat_button = st.button("🗑️ Clear", use_container_width=True, on_click=clear_chat)
    
    # **TIP 6: Additional chat controls**
    if st.session_state.chat_messages:  # Only show controls if there's a conversation
        render_chat_controls()
    
    # **TIP 7: Process user input**
    if user_input:
        # Add user message to chat
        st.session_state.chat_messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # Generate AI response with spinner
        with st.spinner("🤖 AI Coach is thinking..."):
            assistant_response = ai_response(user_input, use_api)
        
        # Add AI response to chat
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # Show any errors that occurred
        if hasattr(st.session_state, 'chat_error'):
            st.warning(st.session_state.chat_error)
            del st.session_state.chat_error
        
        # Trigger rerun to display the new messages
        st.rerun()

def generate_chat_response_api(user_message, initial_context, debate_topic, chat_history):
    """
    Generate AI response using the FastAPI backend
    Note: Falls back to direct Azure connection if API is not available
    """
    try:
        # Prepare chat history for API
        api_history = [
            {"role": msg["role"], "content": msg["content"]} 
            for msg in chat_history[:-1]  # Exclude current message
        ]
        
        response = requests.post(CHAT_API_URL, json={
            "user_message": user_message,
            "initial_context": initial_context,
            "debate_topic": debate_topic,
            "chat_history": api_history
        }, timeout=10)  # Add timeout to prevent hanging
        
        if response.status_code == 200:
            return response.json().get("response", "Sorry, I couldn't generate a response.")
        else:
            error_msg = response.json().get("error", "Unknown API error")
            raise Exception(f"API Error: {error_msg}")
            
    except requests.exceptions.ConnectionError:
        # API server not running - fall back to direct method
        st.info("🔄 API server not available, using direct Azure connection...")
        return generate_chat_response_direct(user_message, initial_context, debate_topic, chat_history)
    except requests.exceptions.Timeout:
        # API timeout - fall back to direct method
        st.warning("⏱️ API timeout, using direct Azure connection...")
        return generate_chat_response_direct(user_message, initial_context, debate_topic, chat_history)
    except Exception as e:
        # Other API errors - fall back to direct method
        st.warning(f"🔄 API issue ({str(e)}), using direct Azure connection...")
        return generate_chat_response_direct(user_message, initial_context, debate_topic, chat_history)

def generate_chat_response_direct(user_message, initial_context, debate_topic, chat_history):
    """
    Generate contextual AI response for the chat (direct Azure connection)
    
    Args:
        user_message (str): User's current message
        initial_context (str): Original feedback/analysis
        debate_topic (str): The debate topic
        chat_history (list): Previous chat messages
    
    Returns:
        str: AI response
    """
    
    # **TIP 9: Build conversation context**
    system_prompt = f"""You are an expert debate coach having a conversation with a student about their debate performance. 

CONTEXT:
- Debate Topic: {debate_topic}
- Initial Analysis: {initial_context[:1000]}...

Your role is to:
1. Provide helpful, specific advice about debate techniques
2. Answer questions about the initial feedback clearly
3. Suggest practical improvement strategies
4. Be encouraging and constructive
5. Keep responses concise but informative (2-3 paragraphs max)

Conversation style:
- Friendly and supportive
- Use relevant examples when helpful
- Focus on actionable advice
- Reference the initial analysis when relevant"""
    
    try:
        messages = st.session_state.chat_messages + [{"role": "system", "content": system_prompt}]
        response = call_ai(messages)
        if not response or response.strip() == "":
            # Handle empty response
            return generate_fallback_response(user_message, initial_context, debate_topic)
        return response
    except Exception as e:
        error_msg = str(e).lower()
        # Better error categorization
        if "authentication" in error_msg or "unauthorized" in error_msg:
            st.error("🔐 Azure OpenAI authentication failed. Please check API credentials.")
        elif "not found" in error_msg or "404" in error_msg:
            st.error("🔍 Azure OpenAI model not found. Please check deployment name.")
        elif "connection" in error_msg or "timeout" in error_msg:
            st.warning("🌐 Connection issue with Azure OpenAI. Using fallback response.")
        else:
            st.warning("⚠️ AI service temporarily unavailable. Using fallback response.")
        
        # Always provide fallback response instead of failing completely
        return generate_fallback_response(user_message, initial_context, debate_topic)

def generate_fallback_response(user_message, initial_context, debate_topic):
    """
    Generate a helpful fallback response when Azure OpenAI is unavailable
    """
    
    # Simple keyword-based responses for common questions
    user_lower = user_message.lower()
    
    if any(word in user_lower for word in ['improve', 'better', 'help']):
        return f"""Based on your analysis for the topic "{debate_topic}", here are some general improvement strategies:

🎯 **Key Areas to Focus On:**
• **Argument Structure**: Use clear claim-warrant-impact format
• **Evidence Quality**: Incorporate recent, credible sources
• **Time Management**: Practice with a timer to optimize pacing
• **Refutation**: Address opponent arguments directly and thoroughly

📚 **Next Steps:**
1. Review your initial feedback carefully
2. Practice specific skills mentioned in the analysis
3. Record yourself again to track progress

*Note: AI coach is temporarily unavailable, but these are proven debate improvement strategies.*"""

    elif any(word in user_lower for word in ['practice', 'exercise', 'drill']):
        return f"""Here are some practice exercises for "{debate_topic}":

🏃‍♂️ **Daily Practice Routine:**
• **5-minute drills**: Argue both sides of your topic
• **Evidence integration**: Practice weaving sources into arguments
• **Timing practice**: Deliver contentions within time limits
• **Refutation practice**: Address common opposing arguments

🎯 **Specific Exercises:**
1. Record 2-minute opening statements
2. Practice transitions between contentions
3. Drill key statistics and evidence
4. Mock cross-examination sessions

*AI coach connection will be restored shortly for personalized feedback.*"""

    elif any(word in user_lower for word in ['strong', 'weak', 'good', 'bad']):
        return f"""Based on your feedback analysis:

💪 **Likely Strengths:**
• Clear topic understanding
• Engagement with the resolution
• Attempt at structured argumentation

🔧 **Areas for Development:**
• Refine argument clarity and flow
• Strengthen evidence integration
• Improve timing and pacing
• Enhance refutation techniques

📊 **General Advice:**
Focus on 2-3 specific improvement areas rather than trying to fix everything at once. Consistent practice with targeted skills will yield better results.

*For detailed, personalized feedback, please try again when the AI coach connection is restored.*"""

    else:
        return f"""Thank you for your question about "{debate_topic}"!

🤖 **AI Coach Status**: Temporarily unavailable

💡 **General Coaching Tips:**
• Review your initial feedback thoroughly
• Focus on one improvement area at a time
• Practice regularly with timing constraints
• Seek feedback from coaches or peers
• Watch exemplary debates for technique examples

🔄 **Try Again**: The personalized AI coach will be available once the connection is restored. Your question was: "{user_message[:100]}..."

*In the meantime, consider reviewing debate fundamentals and practicing core skills.*"""

def render_chat_suggestions():
    """Render suggested questions to help users start the conversation"""
    
    st.markdown("#### 💡 Suggested Questions")
    
    col1, col2 = st.columns(2)
    
    suggestions = [
        "How can I improve my argument structure?",
        "What are the strongest points in my case?", 
        "How can I better address counterarguments?",
        "What should I focus on practicing next?",
        "Can you explain the feedback about my pacing?",
        "How do I make my impacts more compelling?"
    ]
    
    for i, suggestion in enumerate(suggestions):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(f"💭 {suggestion}", key=f"suggestion_{i}", use_container_width=True):
                # Add suggestion to chat input
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": suggestion
                })

def render_chat_metrics():
    """Display chat metrics and engagement stats"""
    
    if "chat_messages" in st.session_state and st.session_state.chat_messages:
        st.markdown("#### 📊 Chat Stats")
        
        col1, col2, col3 = st.columns(3)
        
        total_messages = len(st.session_state.chat_messages)
        user_messages = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
        
        with col1:
            st.metric("💬 Total Messages", total_messages)
        
        with col2:
            st.metric("❓ Your Questions", user_messages)
        
        with col3:
            avg_length = sum(len(m["content"]) for m in st.session_state.chat_messages) // total_messages if total_messages > 0 else 0
            st.metric("📝 Avg Length", f"{avg_length} chars")

def export_chat_conversation():
    """Export chat conversation to text format"""
    if "chat_messages" in st.session_state and st.session_state.chat_messages:
        conversation = f"Debate Topic: {st.session_state.chat_topic}\n"
        conversation += f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        conversation += "="*50 + "\n\n"
        
        for i, message in enumerate(st.session_state.chat_messages):
            role = "You" if message["role"] == "user" else "AI Coach"
            conversation += f"{role}: {message['content']}\n\n"
        
        return conversation
    return "No conversation to export."

def render_chat_controls():
    """Render additional chat controls and features"""
    st.markdown("#### ⚙️ Chat Controls")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📥 Export Chat", use_container_width=True):
            if "chat_messages" in st.session_state and st.session_state.chat_messages:
                chat_export = export_chat_conversation()
                st.download_button(
                    label="💾 Download Chat",
                    data=chat_export,
                    file_name=f"chat_session_{int(time.time())}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("No chat history to export")
    
    with col2:
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
    
    with col3:
        if st.button("📊 Chat Stats", use_container_width=True):
            render_chat_metrics()
    
    with col4:
        if st.button("💡 Get Tips", use_container_width=True):
            render_chat_suggestions()