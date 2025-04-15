from asyncpg import Connection
from fastapi import Depends

from app.dependencies.db import get_db_connection
from app.dependencies.repository import get_auth_repository, get_tdx_repository
from app.repositories.auth_repository import AuthRepositoryInterface
from app.repositories.tdx_repository import TdxRepositoryInterface
from app.services.tdx import TdxClient
from app.use_cases.auth import AuthUseCase, AuthUseCaseInterface
from app.use_cases.tdx import TdxUseCase, TdxUseCaseInterface


async def get_auth_use_case(
    auth_repository: AuthRepositoryInterface = Depends(get_auth_repository),
) -> AuthUseCaseInterface:
    return AuthUseCase(auth_repository=auth_repository)


def get_tdx_use_case(
    tdx_repository: TdxRepositoryInterface = Depends(get_tdx_repository),
    conn: Connection = Depends(get_db_connection),
) -> TdxUseCaseInterface:
    return TdxUseCase(TdxClient(), tdx_repository, conn)
