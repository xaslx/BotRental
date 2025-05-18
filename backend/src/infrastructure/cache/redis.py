from redis.asyncio import Redis
from typing import Any
from src.infrastructure.cache.base import BaseCacheService


class RedisCacheService(BaseCacheService):
    def __init__(
        self,
        host: str = 'redis',
        port: int = 6379,
        db: int = 0,
        decode_responses: bool = True,
        **kwargs
    ):

        self._client = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
            **kwargs
        )

    async def get(self, key: str) -> Any | None:

        return await self._client.get(key)

    async def set(self, key: str, value: Any, **kwargs) -> bool:

        return await self._client.set(key, value, **kwargs)

    async def set_with_ttl(self, key: str, value: Any, ttl_seconds: int) -> bool:

        return await self._client.setex(key, ttl_seconds, value)
    
    async def delete(self, key: str) -> int:
        
        return await self._client.delete(key)


    @property
    def client(self) -> Redis:

        return self._client