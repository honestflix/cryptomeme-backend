from pydantic import BaseModel, Field

class ImageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    cfg_scale: int = Field(default=2, ge=1, le=10)
    height: int = Field(default=1024, ge=64, le=2048)
    width: int = Field(default=1024, ge=64, le=2048)
    steps: int = Field(default=8, ge=1, le=50)
    engine: str = Field(default="proteus")
