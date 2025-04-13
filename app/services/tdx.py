import time
from typing import Optional

import httpx
from redis.exceptions import RedisError

from app.infra.redis import redis_client
from config.config import get_settings

settings = get_settings()


class TdxAuthenticateError(Exception):
    pass


class TdxClient:
    def __init__(self):
        self.redis = redis_client
        self.token_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
        self.client_id = settings.TDX_CLIENT_ID
        self.client_secret = settings.TDX_CLIENT_SECRET
        self.redis_key = "tdx_access_token"
        self.redis_lock_key = f"{self.redis_key}:lock"

    async def request(self, method: str, url: str, **kwargs):
        token = await self._get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        response = httpx.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:
            await self._refresh_token_with_lock()
            return await self.request(method, url, **kwargs)

        return response.json()

    async def _get_access_token_from_cache(self) -> Optional[str]:
        try:
            token = await self.redis.get(self.redis_key)
            if token:
                return str(token)
            return None
        except RedisError as e:
            return None

    async def _get_refresh_token_lock(self) -> bool:
        try:
            return bool(await self.redis.set(self.redis_lock_key, "1", nx=True, ex=5))
        except RedisError as e:
            return True

    async def _delete_refresh_token_lock(self):
        try:
            await self.redis.delete(self.redis_lock_key)
        except RedisError as e:
            return None

    async def _cache_access_token(self, token: str, expires_in: int):
        try:
            await self.redis.setex(self.redis_key, expires_in - 30, token)
        except RedisError as e:
            return None

    async def _get_access_token(self) -> str:
        token = await self._get_access_token_from_cache()
        if token is not None:
            return token
        return await self._refresh_token_with_lock()

    async def _refresh_token_with_lock(self) -> str:
        if await self._get_refresh_token_lock():
            try:
                return await self._refresh_token()
            except httpx.HTTPStatusError as e:
                raise TdxAuthenticateError("Failed to get access token.")
            finally:
                await self._delete_refresh_token_lock()
        else:
            for _ in range(10):
                time.sleep(1)
                token = await self._get_access_token_from_cache()
                if token is not None:
                    return token
            raise TdxAuthenticateError(
                "Failed to get access token after waiting for lock."
            )

    async def _refresh_token(self) -> str:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = httpx.post(self.token_url, data=data)
        response.raise_for_status()
        result = response.json()
        access_token = result["access_token"]
        expires_in = result["expires_in"]
        await self._cache_access_token(access_token, expires_in)
        return access_token
