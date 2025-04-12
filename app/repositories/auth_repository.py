from abc import ABC, abstractmethod
from typing import Optional

from asyncpg.exceptions import UniqueViolationError

from app.schemas.user import User


class DuplicateUserError(Exception):
    pass


class AuthRepositoryInterface(ABC):
    @abstractmethod
    async def register(self, username: str, email: str, hashed_password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError


INSERT_USER_QUERY = """
    INSERT INTO users (username, email, password)
    VALUES ($1, $2, $3)
    RETURNING id
"""

GET_USER_BY_USERNAME_QUERY = """
    SELECT id, username, email, password 
    FROM users 
    WHERE username = $1
"""


class AuthRepository(AuthRepositoryInterface):
    def __init__(self, conn):
        self.conn = conn

    async def register(self, username: str, email: str, hashed_password: str) -> None:
        try:
            await self.conn.execute(INSERT_USER_QUERY, username, email, hashed_password)
        except UniqueViolationError:
            raise DuplicateUserError("username, email or password already exists")

    async def get_user_by_username(self, username: str) -> Optional[User]:
        row = await self.conn.fetchrow(GET_USER_BY_USERNAME_QUERY, username)
        if row:
            return User(**row)
        return None
