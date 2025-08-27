from fastapi import FastAPI, UploadFile, HTTPException, status, Request
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from collections import defaultdict
from pydantic import BaseModel
from google import genai
from typing import Dict
from uuid import uuid4
import pypdf
import logging
import os

app = FastAPI()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_store : Dict[str, str] = {}

logger = logging.getLogger(__name__)

class FileUpload(BaseModel):
    base64_string: str

# Rate limiter storage and settings
rate_limit_data: Dict[str, list] = defaultdict(list)
RATE_LIMIT = 20
TIME_WINDOW = timedelta(minutes=1)

# Rate limiter function
def rate_limiter(request: Request):
    if(request.client == None): 
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Client could not be identified.")

    client_ip = request.client.host
    now = datetime.now()

    # Cleanup old requests beyond the time window
    rate_limit_data[client_ip] = [timestamp for timestamp in rate_limit_data[client_ip] if now - timestamp < TIME_WINDOW]

    # Enforce rate limiting
    if len(rate_limit_data[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded.")

    # Log the current request
    rate_limit_data[client_ip].append(now)

# Include middleware to enforce rate limiter
@app.middleware('http')
async def add_rate_limit(request: Request, call_next):
    try:
        rate_limiter(request)
        response = await call_next(request)
    except HTTPException as e:
        response = JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    return response

# Route responsible for the upload of pdf/txt files
@app.post('/upload')
async def upload_file(file: UploadFile):
    try:
        file_id = str(uuid4())  # Generate unique file ID
        file_path = ""

        if(file.content_type == 'application/pdf'):
            file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
        else:
            file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.txt")

        with open(file_path, 'wb') as output_file:
            output_file.write(await file.read())

        file_store[file_id] = file_path  # Store file path
        return JSONResponse(content={"file_id": file_id, "file_path": file_path}, status_code=200)
    except Exception as e:
        # Log and return error in case of failure
        logger.error(f"File upload failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Route responsible for extracting the text from the pdf/txt file and call the LLM api to request a classification and reply
@app.get('/classify')
async def upload_info(file_id: str):
    try:
        if file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = file_store[file_id];
        extracted_email = ""

        # Checks if the file stored is a pdf or txt file
        if(file_path.find('.pdf') != -1):
            reader = pypdf.PdfReader(file_path)
            extracted_email = reader.pages[0].extract_text()
        else:
            with open(file_path, 'rt') as output_file:
                extracted_email = output_file.read()

        # Calls the LLM api to request a generative text content based on the input from the extracted text
        response = client.models.generate_content(
             model="gemini-2.5-flash", contents="Only return the classification for the following email text as Productive or Unproductive(create an appropriate response for the sender with no line breaks): " + extracted_email
        )

        if(response.text == None):
            raise HTTPException(status_code=500, detail="Error getting response for AI model server.") 

        if "Productive" in response.text:
            classification = "Productive"
        else:
            classification = "Unproductive"

        reply = response.text[len(classification):len(response.text)]

        return JSONResponse(content={'classification': classification, 'reply': reply}, status_code=200)        
    except Exception as e:
        logger.error(f"Header extraction failed: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)