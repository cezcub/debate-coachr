import os
import tempfile
from fastapi import UploadFile, APIRouter, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import whisper
from backend.azure import pf_feedback

router = APIRouter()

@router.post("/transcribe/")
async def transcribe_endpoint(file: UploadFile = File(...), model=whisper.load_model("tiny.en"), debate_topic: str = ""):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # Convert the audio file to WAV format
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            AudioSegment.from_file(temp_audio_path).export(temp_wav.name, format="wav")
            temp_wav_path = temp_wav.name

        # Transcribe the audio using Whisper
        transcription = model.transcribe(temp_wav_path)["text"]

        # Clean up temporary files
        os.remove(temp_audio_path)
        os.remove(temp_wav_path)

        # Process the transcription with Azure OpenAI
        azure_output = pf_feedback(debate_topic, transcription)
    
        return JSONResponse(
            content={"azure_output": azure_output},
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)