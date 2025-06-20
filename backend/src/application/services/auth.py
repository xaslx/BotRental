from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.application.services.jwt import JWTService
from src.domain.user.exception import UserIsNotPresentException, UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity
import orjson
import logging
from src.infrastructure.cache.base import BaseCacheService
import orjson


logger = logging.getLogger(__name__)




@dataclass
class BaseAuthService(ABC):
    
    _user_repository: BaseUserRepository
    _jwt_service: JWTService
    _cache_service: BaseCacheService

    @abstractmethod
    async def authenticate_user(self, telegram_id: int) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_current_user(self, token: str) -> UserEntity | None:
        ...



@dataclass
class AuthServiceImpl(BaseAuthService):

    async def authenticate_user(self, telegram_id: int) -> UserEntity | None:
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(telegram_id=telegram_id)

        if not user:
            raise UserNotFoundException()
        
        return user

    async def get_current_user(self, token: str) -> UserEntity | None:

        payload: dict | None = self._jwt_service.verify_access_token(token=token)

        if not payload or payload.get('type') != 'access':
            return None
        
        user_tg_id: str | None = payload.get('sub')

        if not user_tg_id:
            return None

        cache_key: str = f'user:{user_tg_id}'
        cached_user: str | None = await self._cache_service.get(cache_key)
        
        if cached_user:
            try:
                user_dict = orjson.loads(cached_user)
                return UserEntity.from_dict(user_dict)
            except orjson.JSONDecodeError:
                logger.error('ORJSON error when loading cached user')

        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(int(user_tg_id))

        if not user:
            raise UserNotFoundException()

        await self._cache_service.set_with_ttl(
            key=cache_key,
            value=orjson.dumps(user.to_dict()),
            ttl_seconds=600
        )

        return user