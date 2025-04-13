from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter

from app.dependencies.auth import get_user
from app.dependencies.use_case import get_tdx_use_case
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
