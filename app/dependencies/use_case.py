from fastapi import Depends

from app.dependencies.repository import get_auth_repository
from app.repositories.auth_repository import AuthRepositoryInterface
from app.use_cases.auth import AuthUseCase


async def get_auth_use_case(
    auth_repository: AuthRepositoryInterface = Depends(get_auth_repository),
) -> AuthUseCase:
    return AuthUseCase(auth_repository=auth_repository)
