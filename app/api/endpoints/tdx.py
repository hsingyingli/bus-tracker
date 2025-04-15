from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, EmailStr, Field

from app.dependencies.auth import get_user
from app.dependencies.use_case import get_tdx_use_case
from app.schemas.user import User
from app.services.tdx import TdxAuthenticateError
from app.use_cases.tdx import TdxUseCaseInterface

router = APIRouter()


@router.get(
    "/bus/estimated_time_of_arrival/city/{city}/{route}",
    dependencies=[
        Depends(RateLimiter(times=5, minutes=1)),
        Depends(get_user),
    ],
)
async def estimated_time_of_arrival(
    city: Annotated[str, Path(title="City", description="City name")],
    route: Annotated[str, Path(title="Route", description="Route name")],
    tdx_use_case: TdxUseCaseInterface = Depends(get_tdx_use_case),
):
    try:
        response = await tdx_use_case.estimated_time_of_arrival(city, route)
        return response
    except TdxAuthenticateError:
        return JSONResponse(
            content={"detail": "Authentication failed"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class Subscription(BaseModel):
    target_stop_uid: str
    email: EmailStr
    notify_before_minutes: int = Field(..., gt=0)
    direction: int = Field(..., ge=0, le=1)


@router.post(
    "/bus/estimated_time_of_arrival/city/{city}/{route}/subscribe",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(RateLimiter(times=5, minutes=1)),
    ],
)
async def subscribe_arrival(
    subscription: Subscription,
    city: Annotated[str, Path(title="City", description="City name")],
    route: Annotated[str, Path(title="Route", description="Route name")],
    tdx_use_case: TdxUseCaseInterface = Depends(get_tdx_use_case),
    user: User = Depends(get_user),
):
    await tdx_use_case.subscribe_arrival(
        user,
        city,
        route,
        subscription.direction,
        subscription.target_stop_uid,
        subscription.notify_before_minutes,
        subscription.email,
    )
