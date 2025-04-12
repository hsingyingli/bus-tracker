from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

import asyncpg

from config.config import get_settings

settings = get_settings()


class Database:
    _instance: Optional["Database"] = None
    db_pool: Optional[asyncpg.Pool] = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def create_pool(self):
        return await asyncpg.create_pool(
            dsn=str(settings.DATABASE_URL),
            min_size=settings.DATABASE_MIN_POOL,
            max_size=settings.DATABASE_MAX_POOL,
            max_queries=settings.DATABASE_MAX_QUERIES,
            max_inactive_connection_lifetime=settings.DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME,
        )

    async def init(
        self,
    ):
        if not self.db_pool:
            self.db_pool = await self.create_pool()

    async def close(self):
        if self.db_pool:
            await self.db_pool.close()

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[asyncpg.Connection]:
        if not self.db_pool:
            await self.init()
        if self.db_pool is None:
            raise Exception("Database pool is not initialized.")
        async with self.db_pool.acquire() as connection:
            yield connection


database = Database()
