# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
from PIL import Image
import io
import base64
import torch

app = FastAPI()

# Load the model from local path
local_path = "./stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(local_path)
pipe = pipe.to("cpu")  # Use "cpu" if you do not have a CUDA-compatible GPU

class MemeRequest(BaseModel):
    text: str

@app.post("/generate-meme")
async def generate_meme(request: MemeRequest):
    try:
        # Generate image
        with torch.no_grad():
            image = pipe(request.text).images[0]

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
