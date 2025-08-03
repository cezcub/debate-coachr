from fileinput import filename
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
from backend.azure import case_feedback
from backend.text_extraction import extract_text_from_file
import tempfile
import os

router = APIRouter()

@router.post("/process-text/")
async def process_text(request: Request, file: UploadFile = File(...), debate_topic: str = "", side: str = "", upload_format: str = "plaintext"):
    """
    Endpoint to process an uploaded text file.
    Supports plaintext, DOCX, and PDF uploads with format-specific processing.
    """
    # Get the raw form data and override parameters to fix FastAPI parsing issue
    try:
        form_data = await request.form()
        
        # Override parameters with actual form data values
        actual_debate_topic = form_data.get("debate_topic", debate_topic)
        actual_side = form_data.get("side", side)
        actual_upload_format = form_data.get("upload_format", upload_format)
        actual_file_extension = form_data.get("file_extension")
        
    except Exception as e:
        # Fallback to original parameters
        actual_debate_topic = debate_topic
        actual_side = side
        actual_upload_format = upload_format
        
    try:
        # Extract text
        extracted_text = extract_text_from_file(file, actual_file_extension, actual_upload_format)

    except ValueError as e:
        return JSONResponse(content={"error": f"File processing error: {str(e)}"}, status_code=400)
        
    # Send to Azure with format information
    # Ensure extracted_text is a string
    if isinstance(extracted_text, bytes):
        try:
            extracted_text = extracted_text.decode('utf-8')
        except UnicodeDecodeError:
            extracted_text = extracted_text.decode('utf-8', errors='replace')
    elif not isinstance(extracted_text, str):
        extracted_text = str(extracted_text)
    
    output = case_feedback(actual_debate_topic, extracted_text, actual_side, actual_upload_format)

    return JSONResponse(content={
        "processed_text": output,
        "extracted_text": extracted_text,  # Add for debugging
        "debug_info": {
            "filename": file.filename,
            "upload_format": actual_upload_format,
            "text_length": len(extracted_text)
        }
    }, status_code=200)