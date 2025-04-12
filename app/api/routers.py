from fastapi import APIRouter

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.tdx import router as tdx_router

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(tdx_router, prefix="/tdx", tags=["tdx"])
