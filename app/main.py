from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
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

    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
