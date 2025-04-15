import redis.asyncio as redis

from config.config import get_settings

settings = get_settings()
redis_client = redis.Redis.from_url(
    str(settings.REDIS_URL), encoding="utf-8", decode_responses=True
)
