from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image
import io
import base64

app = FastAPI()

generator = pipeline('text-to-image-generation', model='CompVis/stable-diffusion-v-1-4', framework='pt')

class MemeRequest(BaseModel):
    text: str

@app.post("/generate-meme")
async def generate_meme(request: MemeRequest):
    try:
        result = generator(request.text, num_return_sequences=1)
        image = result[0]['image']
        
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return {"image": img_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
