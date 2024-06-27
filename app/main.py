# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image
import io
import base64
import os
from huggingface_hub import login
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Get Hugging Face access token from environment variable
HUGGINGFACE_ACCESS_TOKEN = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

if not HUGGINGFACE_ACCESS_TOKEN:
    raise ValueError("Hugging Face access token is not set in the environment variables")

login(token=HUGGINGFACE_ACCESS_TOKEN)

# Load the model
generator = pipeline('text-to-image', model='stabilityai/stable-diffusion-2-1', use_auth_token=HUGGINGFACE_ACCESS_TOKEN, framework='pt')

class MemeRequest(BaseModel):
    text: str

@app.post("/generate-meme")
async def generate_meme(request: MemeRequest):
    try:
        # Generate image
        result = generator(request.text, num_return_sequences=1)
        image = result[0]['image']

        # Convert PIL image to base64 string
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return {"image": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
