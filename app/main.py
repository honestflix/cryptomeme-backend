# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from app.models.request import ImageRequest
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.post("/generate-image/")
def generate_image(request: ImageRequest):
    url = "https://api.corcel.io/v1/image/vision/text-to-image"

    api_key = os.getenv("API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is missing")
    
    payload = {
        "text_prompts": [prompt.dict() for prompt in request.text_prompts],
        "cfg_scale": request.cfg_scale,
        "height": request.height,
        "width": request.width,
        "steps": request.steps,
        "engine": request.engine
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
