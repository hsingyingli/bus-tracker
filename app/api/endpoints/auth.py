from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from app.dependencies.use_case import get_auth_use_case
from app.use_cases.auth import AuthUseCaseInterface, RegisterUserError

router = APIRouter()


class RegisterForm(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
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
