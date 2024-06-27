from fastapi import FastAPI, WebSocket, HTTPException
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
class CryptoMeme():
    
    def __init__(self):
        super().__init__()
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

                data = response.json()
                # image_response = utility_models.ImageResponseBody(**data)
                # return image_response
                return data

            except httpx.HTTPStatusError as error:
                    f"Error getting an image; response {error.response.status_code} while making request to {endpoint}: {error}"
            
            except httpx.RequestError as error:
                    f"Error getting an image; An error occurred while making request to {endpoint}: {error}"

    async def text_to_image(self, private_input):
        POST_ENDPOINT = 'text-to-image'
        body = {
            "cfg_scale": 2,
            "height": private_input.height,
            "width": private_input.width,
            "steps": 8,
            "engine": "proteus",
            "text_prompts": [{"text": private_input.prompt}]
        }

        image_response_body = await self.get_image_from_server(body, POST_ENDPOINT, timeout=15)
        return image_response_body
    
    async def image_to_image(self, private_input):
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

        image_response_body = await self.get_image_from_server(body, POST_ENDPOINT, timeout=15)
        return image_response_body

    async def forward(self, private_input, timeout: float):
        if private_input.type == 'txt2img':
            return await self.text_to_image(private_input)
        elif private_input.type == 'img2img':
            return await self.image_to_image(private_input)

    async def run(self, private_input):
        response = await self.forward(private_input,60)
        return response