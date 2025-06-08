from src.infrastructure.repositories.user.base import BaseUserRepository, T
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.user import User
from sqlalchemy import select
import logging


logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    
    _session: AsyncSession

    async def add(self, entity: UserEntity) -> UserEntity:

        try:
            model: User = User.from_entity(entity=entity)
            self._session.add(model)
            await self._session.commit()
            return model.to_entity()
        except Exception as e:
            logger.error(f'Ошибка при добавлении пользователя: {entity} в БД: {e}')
            raise e

    
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:

        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user: User | None = result.scalar_one_or_none()

        if user:
            return user.to_entity()
        
        return None
    
    async def update(self, entity: UserEntity) -> UserEntity:

        result = await self._session.execute(
            select(User).where(User.id == entity.id)
        )
        user_model = result.scalar_one()
        
        user_model.is_deleted = entity.is_deleted
        user_model.is_active = entity.is_active
        user_model.balance = entity.balance.value

        await self._session.commit()
        await self._session.refresh(user_model)
        
        return user_model.to_entity()
    
    async def delete(self, entity: UserEntity) -> UserEntity:
        return await super().delete(entity)