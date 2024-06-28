from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import List
import logging

class ImageRequest(BaseModel):
    text: str
    cfg_scale: int = 2
    height: int = 1024
    width: int = 1024
    steps: int = 8
    engine: str = "proteus"

# Load environment variables
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS Middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API configuration
COEL_API_URL = "https://api.corcel.io/v1/image/vision/text-to-image"
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Missing required environment variable: TOKEN")

# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    logger.info(f"New request: {request.method} {request.url}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Client IP: {client_ip}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")
    return response

@app.post("/generate")
async def generate_image(request: Request, image_request: ImageRequest):
    client_ip = request.client.host
    payload = {
        "text_prompts": [
            {
                "text": image_request.text,
                "weight": 0
            }
        ],
        "cfg_scale": image_request.cfg_scale,
        "height": image_request.height,
        "width": image_request.width,
        "steps": image_request.steps,
        "engine": image_request.engine
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": TOKEN
    }

    response = requests.post(COEL_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response_json = response.json()

    new_entry = {
        "text": image_request.text,
        "created_at": datetime.utcnow().isoformat(),
        "client_ip": client_ip,
        "response": response_json
    }

    # Load existing data and append the new entry
    try:
        with open("response.json", "r") as json_file:
            data = json.load(json_file)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    # Save updated data back to the file
    with open("response.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    return response_json

@app.get("/images")
async def get_images() -> List[dict]:
    try:
        with open("response.json", "r") as json_file:
            data = json.load(json_file)
            if not isinstance(data, list):
                data = []
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No images found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error reading the JSON file")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
