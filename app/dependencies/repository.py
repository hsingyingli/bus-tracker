from asyncpg import Connection
from fastapi import Depends

from app.dependencies.db import get_db_connection
from app.repositories.auth_repository import AuthRepository


async def get_auth_repository(
    conn: Connection = Depends(get_db_connection),
) -> AuthRepository:
    return AuthRepository(conn=conn)
