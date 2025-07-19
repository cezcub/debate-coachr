from fastapi import FastAPI
import whisper
import os
from dotenv import load_dotenv
from backend.transcription import router as audio_router
from backend.case import router as text_router

# Load environment variables at startup
load_dotenv()

app = FastAPI()

# Load the Whisper model once during startup
model = whisper.load_model("tiny.en")

# Include the Audio Feedback router
app.include_router(audio_router)

# Include the text processing router
app.include_router(text_router)