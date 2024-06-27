from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import List

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
router = APIRouter()

# Configuration constants
COEL_API_URL = "https://api.corcel.io/v1/image/vision/text-to-image"
TOKEN = os.getenv("TOKEN")
IMAGE_FILE_PATH = "app/data/images.json"

# Validate TOKEN
if not TOKEN:
    raise ValueError("API token is missing. Please set the TOKEN environment variable.")

# Pydantic models
class ImageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    cfg_scale: int = Field(default=2, ge=1, le=10)
    height: int = Field(default=1024, ge=64, le=2048)
    width: int = Field(default=1024, ge=64, le=2048)
    steps: int = Field(default=8, ge=1, le=50)
    engine: str = Field(default="proteus")

class ImageDetails(BaseModel):
    url: str
    creation_date: datetime
    prompt: str

class ImageList(BaseModel):
    images: List[ImageDetails]

# Utility functions
def save_image_details(url: str, prompt: str):
    try:
        with open(IMAGE_FILE_PATH, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"images": []}

    image_details = ImageDetails(url=url, creation_date=datetime.utcnow(), prompt=prompt)
    data["images"].append(image_details.dict())

    os.makedirs(os.path.dirname(IMAGE_FILE_PATH), exist_ok=True)
    with open(IMAGE_FILE_PATH, "w") as file:
        json.dump(data, file, default=str, indent=4)

def load_image_details() -> List[ImageDetails]:
    try:
        with open(IMAGE_FILE_PATH, "r") as file:
            data = json.load(file)
        return ImageList(**data).images
    except FileNotFoundError:
        return []

# Route to generate image
@router.post("/generate")
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

    response_data = response.json()
    image_url = response_data.get("url")  # Assuming the response contains the URL in the "url" field

    if not image_url:
        raise HTTPException(status_code=500, detail="Image URL not found in the response")

    # Save the image details
    save_image_details(url=image_url, prompt=request.text)
    
    return response_data

# Route to list generated images
@router.get("/list", response_model=List[ImageDetails])
async def list_images():
    images = load_image_details()
    return images

# Include router in the FastAPI app
app.include_router(router)

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
