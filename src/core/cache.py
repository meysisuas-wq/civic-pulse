from typing import Optional, Any
import json, structlog
from src.config import settings

logger = structlog.get_logger()
_redis = None

async def init_cache():
    global _redis
    try:
        import redis.asyncio as aioredis
        _redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        await _redis.ping()
        logger.info("Redis cache connected")
    except Exception as e:
        logger.warning("Redis connection failed", error=str(e))

async def get_cache(key: str) -> Optional[Any]:
    if _redis is None: return None
    try:
        v = await _redis.get(key)
        return json.loads(v) if v else None
    except: return None

async def set_cache(key: str, value: Any, ttl: int = None):
    if _redis is None: return
    if ttl is None: ttl = settings.REDIS_CACHE_TTL
    try: await _redis.set(key, json.dumps(value), ex=ttl)
    except: pass

async def delete_cache(key: str):
    if _redis:
        try: await _redis.delete(key)
        except: pass
