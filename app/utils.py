import logging
import json
from datetime import datetime
from typing import List
from app.models import ImageDetails, ImageList

IMAGE_FILE_PATH = "app/data/images.json"

def save_image_details(url: str, prompt: str):
    try:
        with open(IMAGE_FILE_PATH, "r") as file:
            image_data = json.load(file)
    except FileNotFoundError:
        data = {"images": []}
        
    image_details = ImageDetails(url=url, creation_date=datetime.utcnow(), prompt=prompt)
    data["images"].append(image_details.dict())
    
    with open(IMAGE_FILE_PATH, "w") as file:
        json.dump(data, file, default=str, indent=4)

def load_image_details() -> List[ImageDetails]:
    try:
        with open(IMAGE_FILE_PATH, "r") as file:
            data = json.load(file)
        return ImageList(**data).images
    except FileNotFoundError:
        return []
    
def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()
