from pydantic import BaseModel
from typing import List

class TextPrompt(BaseModel):
    text: str
    weight: int

class ImageRequest(BaseModel):
    text_prompts: List[TextPrompt]
    cfg_scale: int
    height: str
    width: str
    steps: int
    engine: str
