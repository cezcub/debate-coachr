from fastapi import FastAPI
import whisper
from backend.transcription import router as audio_router
from backend.case import router as text_router
from backend.chat import router as chat_router

app = FastAPI()

# Load the Whisper model once during startup
model = whisper.load_model("tiny.en")

# Include the Audio Feedback router
app.include_router(audio_router)

# Include the text processing router
app.include_router(text_router)

# Include the chat router
app.include_router(chat_router)