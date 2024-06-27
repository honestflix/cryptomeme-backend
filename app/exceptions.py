from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import HTTPException

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
