from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.main import CryptoMeme

from fastapi import UploadFile, File, HTTPException, Body
import asyncio
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MemeItem(BaseModel):
    type: str
    prompt: str
    width: Optional[int] = 512
    height: Optional[int] = 512
    init_image: Optional[str] = ''


@app.post("/meme/")
async def meme(item: MemeItem):
    return await CryptoMeme.run(item, private_input=[])


