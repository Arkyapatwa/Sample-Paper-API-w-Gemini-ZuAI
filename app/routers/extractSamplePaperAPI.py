from fastapi import APIRouter, HTTPException, UploadFile, Body, File
from fastapi.responses import JSONResponse
from app.internal.extractSamplePaper import extract_from_pdf, extract_from_text
import os, shutil

router = APIRouter()
UPLOAD_DIR = "./app/uploads"


@router.post("/extract/pdf")
async def extract_pdf(pdf_file: UploadFile = File(...)):
    """
    API to extract sample paper from pdf
    """
    try:
        print(pdf_file.filename)
        if pdf_file.content_type != "application/pdf":
            return JSONResponse(status_code=400, content="Invalid file type. Please upload a PDF file.")

        # save file
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
            
        file_location = f"{UPLOAD_DIR}/{pdf_file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
            
        response_json = await extract_from_pdf(file_location)
        return JSONResponse(status_code=200, content=response_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong: " + str(e))
    

@router.post("/extract/text")
def extract_text(text: str = Body(...)):
    """
    API to extract sample paper from text
    """
    
    try:
        if text is None:
            return JSONResponse(status_code=400, content="Invalid text. Please provide a valid text.")
        
        response_json = extract_from_text(text)
        return JSONResponse(status_code=200, content=response_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong: " + str(e))