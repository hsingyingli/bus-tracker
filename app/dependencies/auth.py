from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.repository import get_auth_repository
from app.repositories.auth_repository import AuthRepositoryInterface
from app.schemas.user import User
from app.utils.token import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(
    token: str = Depends(oauth2_scheme),
    auth_repository: AuthRepositoryInterface = Depends(get_auth_repository),
) -> User:
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="User not found")
    user = await auth_repository.get_user_by_username(payload["sub"])
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
