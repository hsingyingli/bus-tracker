import secrets
from functools import lru_cache

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    DATABASE_URL: PostgresDsn = PostgresDsn(
        "postgresql://test:testsecret@localhost:5432/bus"
    )
    DATABASE_MAX_POOL: int = 10
    DATABASE_MIN_POOL: int = 1
    DATABASE_MAX_QUERIES: int = 50000
    DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME: int = 300

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"

    REDIS_URL: RedisDsn = RedisDsn("redis://localhost:6379/0")

    # TDX settings
@lru_cache()
def get_settings() -> Settings:
    return Settings()
