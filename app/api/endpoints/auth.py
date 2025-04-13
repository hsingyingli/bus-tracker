from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, EmailStr

from app.dependencies.use_case import get_auth_use_case
from app.use_cases.auth import (AuthUseCaseInterface, RegisterUserError,
                                UserNotFoundError, UserPasswordMismatchError)

router = APIRouter()


class RegisterForm(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(RateLimiter(times=5, minutes=1)),
    ],
)
async def register(
    form_data: RegisterForm,
    auth_use_case: AuthUseCaseInterface = Depends(get_auth_use_case),
):
    try:
        await auth_use_case.register(
            form_data.username, form_data.email, form_data.password
        )
    except RegisterUserError:
        return JSONResponse(
            content={"detail": "User with this username already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post(
    "/login",
    dependencies=[
        Depends(RateLimiter(times=5, minutes=1)),
    ],
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthUseCaseInterface = Depends(get_auth_use_case),
):
    try:
        access_token = await auth_use_case.login(
            username=form_data.username,
            password=form_data.password,
        )
        return JSONResponse(
            content={"access_token": access_token, "token_type": "bearer"},
            status_code=status.HTTP_200_OK,
        )
    except UserNotFoundError:
        return JSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except UserPasswordMismatchError:
        return JSONResponse(
            content={"detail": "Incorrect password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
