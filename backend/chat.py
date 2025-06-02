from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.azure import call_ai
from typing import List, Dict

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_message: str
    initial_context: str
    debate_topic: str
    chat_history: List[ChatMessage] = []

@router.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat requests for real-time discussion with AI coach
    """
    try:
        # Build system prompt for debate coaching context
        system_prompt = f"""You are an expert debate coach having a conversation with a student about their debate performance. 

CONTEXT:
- Debate Topic: {request.debate_topic}
- Initial Analysis: {request.initial_context[:1000]}...

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

        # Build conversation context from history
        conversation_context = ""
        if request.chat_history:
            recent_messages = request.chat_history[-6:]  # Last 6 messages for context
            for msg in recent_messages:
                role = "Student" if msg.role == "user" else "Coach"
                conversation_context += f"{role}: {msg.content}\n"

        # Enhanced user prompt with context
        enhanced_prompt = f"""Previous conversation:
{conversation_context}

Current student question: {request.user_message}

Please provide a helpful response as their debate coach."""

        # Generate AI response
        ai_response = call_ai(system_prompt, enhanced_prompt)
        
        return JSONResponse(
            content={"response": ai_response},
            status_code=200
        )
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Chat error: {str(e)}"},
            status_code=500
        )
