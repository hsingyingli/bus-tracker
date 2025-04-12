from abc import ABC, abstractmethod

from asyncpg.exceptions import UniqueViolationError


class DuplicateUserError(Exception):
    pass


class AuthRepositoryInterface(ABC):
    @abstractmethod
    async def register(self, username: str, email: str, hashed_password: str) -> None:
        raise NotImplementedError


INSERT_USER_QUERY = """
    INSERT INTO users (username, email, password)
    VALUES ($1, $2, $3)
    RETURNING id
"""


class AuthRepository(AuthRepositoryInterface):
    def __init__(self, conn):
        self.conn = conn

    async def register(self, username: str, email: str, hashed_password: str) -> None:
        try:
            await self.conn.execute(INSERT_USER_QUERY, username, email, hashed_password)
        except UniqueViolationError:
            raise DuplicateUserError("username, email or password already exists")
