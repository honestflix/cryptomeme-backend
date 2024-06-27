from fastapi import APIRouter, HTTPException
import requests
from typing import List
from app.models import ImageRequest, ImageDetails
from app.config import COEL_API_URL, TOKEN
from app.utils import logger, save_image_details, load_image_details

router = APIRouter()

@router.post("/generate")
async def generate_image(request: ImageRequest):
    logger.info(f"Received request: {request}")
    
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
        logger.error(f"Error response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response_data = response.json()
    image_url = response_data.get("url")  # Assuming the response contains the URL in the "url" field

    if not image_url:
        raise HTTPException(status_code=500, detail="Image URL not found in the response")

    # Save the image details
    save_image_details(url=image_url, prompt=request.text)
    
    logger.info(f"Response: {response_data}")
    return response_data

@router.get("/list", response_model=List[ImageDetails])
async def list_images():
    images = load_image_details()
    return images
