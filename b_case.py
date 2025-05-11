from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from b_azure import case_feedback

router = APIRouter()

@router.post("/process-text/")
async def process_text(file: UploadFile = File(...)):
    """
    Endpoint to process an uploaded text file.
    """
    try:
        # Read the content of the uploaded text file
        content = await file.read()
        text = content.decode("utf-8")

        # Send to Azure
        output = case_feedback(text)
        # For now, we'll just return the text as-is

        return JSONResponse(content={"processed_text": output}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)