from fastapi import FastAPI, File, UploadFile
import whisper
from backend.transcription import router as fb_router
from backend.case import router as text_router

app = FastAPI()

# Load the Whisper model once during startup
model = whisper.load_model("tiny.en")

# Include the Audio Feedback router
app.include_router(fb_router)

# Include the text processing router
app.include_router(text_router)