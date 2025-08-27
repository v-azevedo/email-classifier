from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google import genai

from uuid import uuid4
import pypdf
import logging
import os

app = FastAPI()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_store = {}

logger = logging.getLogger(__name__)

class FileUpload(BaseModel):
    base64_string: str

@app.post('/upload')
async def upload_file(file: UploadFile):
    try:
        file_id = str(uuid4())  # Generate unique file ID
        
        file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}-converted_pdf.pdf")
        
        with open(file_path, 'wb') as output_file:
            output_file.write(await file.read())

        file_store[file_id] = file_path  # Store file path
        return JSONResponse(content={"file_id": file_id, "file_path": file_path}, status_code=200)
    except Exception as e:
        # Log and return error in case of failure
        logger.error(f"File upload failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get('/classify')
async def upload_info(file_id: str):
    try:
        if file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = file_store[file_id]
        reader = pypdf.PdfReader(file_path)

        response = client.models.generate_content(
             model="gemini-2.5-flash", contents="Only return the classification for the following email text as Productive or Unproductive(create an appropriate response for the sender with no line breaks): " + reader.pages[0].extract_text()
        )

        if(response.text == None):
            raise HTTPException(status_code=500, detail="Error getting response for AI model server.") 

        if "Productive" in response.text:
            classification = "Productive"
        else:
            classification = "Unproductive"

        reply = response.text[len(classification):len(response.text) - 1]

        return JSONResponse(content={'classification': classification, 'reply': reply}, status_code=200)        
    except Exception as e:
        logger.error(f"Header extraction failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)