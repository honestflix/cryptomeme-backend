from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import List

class ImageRequest(BaseModel):
    text: str
    cfg_scale: int = 2
    height: int = 1024
    width: int = 1024
    steps: int = 8
    engine: str = "proteus"

load_dotenv()

app = FastAPI()

COEL_API_URL = "https://api.corcel.io/v1/image/vision/text-to-image"
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Missing required environment variable: TOKEN")

@app.post("/generate")
async def generate_image(request: ImageRequest):
    payload = {
        "text_prompts": [
            {
                "text": request.text,
                "weight": 0
            }
        ],
        "cfg_scale": request.cfg_scale,
        "height": request.height,
        "width": request.width,
        "steps": request.steps,
        "engine": request.engine
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
        "text": request.text,
        "created_at": datetime.utcnow().isoformat(),
        "response": response_json
    }
    
    try:
        with open("response.json", "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)
    
    # Save response JSON to a file
    with open("response.json", "w") as json_file:
        json.dump(response_json, json_file)

    return response_json

@app.get("/images")
async def get_images() -> List[dict]:
    try:
        with open("response.json", "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No images found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error reading the JSON file")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
