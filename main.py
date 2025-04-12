from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import api_router
from config.config import get_settings

settings = get_settings()


app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(api_router)
