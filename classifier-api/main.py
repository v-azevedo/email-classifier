from fastapi import FastAPI, UploadFile, HTTPException, status, Request
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from collections import defaultdict
from pydantic import BaseModel
from google import genai
from typing import Dict
import tempfile
import pypdf
import os

app = FastAPI()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

class Email(BaseModel):
    text: str

# Calls the LLM API to request a generative text content based on the input from the extracted email text
def llm_request(input: str):
    response = client.models.generate_content(
            model="gemini-2.5-flash", contents="Only return the classification for the following email text as Productive or Unproductive(create an appropriate response for the sender with no line breaks): " 
            + input
    )
    
    if(response.text == None):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error getting response for AI model server.") 

    # Checks if the either the productive or unproductive are present in the llm output and pass to the classification var
    if "Productive" in response.text:
        classification = "Productive"
    else:
        classification = "Unproductive"

    # Cuts from the llm response text the classification leaving only the reply
    reply = response.text[len(classification):len(response.text)]

    return classification, reply

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

# Route responsible for extracting the text from the pdf/txt file and call the LLM api to request a classification and reply
@app.post("/classify-upload")
async def upload_file(file: UploadFile | None = None):
    try:
        if(file == None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data was passed, try again to either upload or input the text to be classified.")
        
        extracted_email = ""
        suffix = '.pdf' if file.content_type == "application/pdf" else ".txt"
        
        # With tempfile lib, check what type of file was uploaded and handle accordingly
        with tempfile.NamedTemporaryFile(suffix=suffix) as output_file:
            output_file.write(await file.read())
            file_name = output_file.name

            if(file_name.find('.pdf') != -1):
                reader = pypdf.PdfReader(output_file)
                extracted_email = reader.pages[0].extract_text()
            else:
                output_file.seek(0)
                extracted_email = output_file.read().decode()
            
            classification, reply = llm_request(extracted_email)

        return JSONResponse(content={'classification': classification, 'reply': reply}, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)

# Route from direct text input from json body
@app.post("/classify-text")
async def upload_email(email: Email | None = None):
    try:
        if(email == None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No email was passed, please try again.")
        if(not email.text.strip()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing populated text field.")
        
        classification, reply = llm_request(email.text)

        return JSONResponse(content={'classification': classification, 'reply': reply}, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)