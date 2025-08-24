from abc import ABC, abstractmethod
from typing import Any


class BaseCacheService(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any | None: ...

    @abstractmethod
    async def set(self, key: str, value: Any, **kwargs) -> bool: ...

    @abstractmethod
    async def set_with_ttl(self, key: str, value: Any, ttl_seconds: int) -> bool: ...

    @abstractmethod
    async def delete(self, key: str) -> int: ...

    @property
    @abstractmethod
    def client(self) -> Any: ...
