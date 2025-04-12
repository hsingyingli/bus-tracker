import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from config.config import get_settings

settings = get_settings()


def _get_current_time():
    return datetime.now(timezone.utc)


def _create_token(
    data: dict, secret_key: str, expire_delta: timedelta, jti: Optional[str] = None
) -> str:
    data["jti"] = str(uuid.uuid4()) if jti is None else jti
    data["exp"] = _get_current_time() + expire_delta
    return jwt.encode(data, secret_key, algorithm=settings.JWT_ALGORITHM)


def _verify_token(token: str, secret_key: str):
    try:
        return jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def create_access_token(username: str) -> str:
    return _create_token(
        {"sub": username},
        settings.ACCESS_SECRET_KEY,
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def verify_access_token(token: str):
    return _verify_token(token, settings.ACCESS_SECRET_KEY)
