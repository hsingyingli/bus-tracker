from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter

from app.api.routers import api_router
from app.infra.database import database
from app.infra.redis import redis_client
from config.config import get_settings

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
