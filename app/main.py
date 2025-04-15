from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter

from app.api.routers import api_router
from config.config import get_settings
from infra.database import database
from infra.redis import redis_client

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init()
    await FastAPILimiter.init(redis_client)
    yield
    await database.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(api_router)
