from fastapi import APIRouter, HTTPException
import requests
from app.models import ImageRequest
from app.config import COEL_API_URL, TOKEN
from app.utils import logger

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

    logger.info(f"Response: {response.json()}")
    return response.json()
