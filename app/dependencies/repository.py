from asyncpg import Connection
from fastapi import Depends

from app.dependencies.db import get_db_connection
from app.repositories.auth_repository import (AuthRepository,
                                              AuthRepositoryInterface)
from app.repositories.tdx_repository import (TdxRepository,
                                             TdxRepositoryInterface)


async def get_auth_repository(
    conn: Connection = Depends(get_db_connection),
) -> AuthRepositoryInterface:
    return AuthRepository(conn=conn)


async def get_tdx_repository(
    conn: Connection = Depends(get_db_connection),
) -> TdxRepositoryInterface:
    return TdxRepository(conn=conn)
