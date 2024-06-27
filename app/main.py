from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import httpx

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class MemeItem(BaseModel):
    type: str
    prompt: str
    width: Optional[int] = 512
    height: Optional[int] = 512
    init_image: Optional[str] = ''

# Define the CryptoMeme class
class CryptoMeme:
    def __init__(self):
        self.api_url = "https://api.corcel.io/v1/image/vision/"
        self.api_key = os.getenv("API_KEY")
        
        if not self.api_key:
            raise HTTPException(status_code=500, detail="API key is missing")

    async def get_image_from_server(self, body, post_endpoint: str, timeout: float = 20.0):
        endpoint = self.api_url + post_endpoint
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": self.api_key
        }
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(endpoint, json=body, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as error:
                raise HTTPException(status_code=error.response.status_code, detail=str(error))
            except httpx.RequestError as error:
                raise HTTPException(status_code=500, detail=str(error))

    async def text_to_image(self, private_input: MemeItem):
        POST_ENDPOINT = 'text-to-image'
        body = {
            "cfg_scale": 2,
            "height": private_input.height,
            "width": private_input.width,
            "steps": 8,
            "engine": "proteus",
            "text_prompts": [{"text": private_input.prompt}]
        }

        return await self.get_image_from_server(body, POST_ENDPOINT, timeout=15)
    
    async def image_to_image(self, private_input: MemeItem):
        POST_ENDPOINT = "image-to-image"
        body = {
            "image_strength": 0.25,
            "cfg_scale": 2,
            "height": private_input.height,
            "width": private_input.width,
            "steps": 8,
            "engine": "proteus",
            "text_prompts": [{"text": private_input.prompt}],
            "init_image": private_input.init_image
        }

        return await self.get_image_from_server(body, POST_ENDPOINT, timeout=15)

    async def forward(self, private_input: MemeItem, timeout: float):
        if private_input.type == 'txt2img':
            return await self.text_to_image(private_input)
        elif private_input.type == 'img2img':
            return await self.image_to_image(private_input)
        else:
            raise HTTPException(status_code=400, detail="Invalid type specified")

    async def run(self, private_input: MemeItem):
        return await self.forward(private_input, 60)

# Define the FastAPI endpoint
@app.post("/meme")
async def create_meme(meme_item: MemeItem):
    crypto_meme = CryptoMeme()
    return await crypto_meme.run(meme_item)
