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
            logger.info(f'Пользователь добавлен: {entity}')
            return model.to_entity()
        except Exception as e:
            await self._session.rollback()
            logger.exception(f'Ошибка при добавлении пользователя: {entity} в БД')
            raise

    async def get_all_users(self) -> list[UserEntity] | None:
        try:
            result = await self._session.execute(select(User))
            users: list[User] = result.scalars().all()
            logger.info(f'Получено пользователей: {len(users)}')
            return [user.to_entity() for user in users] if users else None
        except Exception as e:
            logger.exception('Ошибка при получении всех пользователей')
            raise

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        try:
            result = await self._session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user: User | None = result.scalar_one_or_none()

            if user:
                logger.info(f'Найден пользователь с telegram_id={telegram_id}')
                return user.to_entity()

            logger.warning(f'Пользователь с telegram_id={telegram_id} не найден')
            return None
        except Exception as e:
            logger.exception(f'Ошибка при получении пользователя с telegram_id={telegram_id}')
            raise

    async def update(self, entity: UserEntity) -> UserEntity | None:
        try:
            result = await self._session.execute(
                select(User).where(User.telegram_id == entity.telegram_id.value)
            )
            user_model: User | None = result.scalar_one_or_none()

            if not user_model:
                logger.warning(f'Пользователь для обновления не найден: {entity.telegram_id}')
                return None

            user_model.balance = entity.balance.value
            user_model.is_active = entity.is_active
            user_model.is_deleted = entity.is_deleted
            user_model.role = entity.role.value

            await self._session.commit()
            await self._session.refresh(user_model)

            logger.info(f'Пользователь обновлён: {entity.telegram_id}')
            return user_model.to_entity()
        except Exception as e:
            await self._session.rollback()
            logger.exception(f'Ошибка при обновлении пользователя: {entity}')
            raise

    async def delete(self, entity):
        try:
            return await super().delete(entity)
        except Exception as e:
            logger.exception(f'Ошибка при удалении пользователя: {entity}')
            raise

    async def save(self, entity: UserEntity) -> None:
        try:
            model = User.from_entity(entity)
            self._session.add(model)
            await self._session.commit()
            logger.info(f'Пользователь сохранён: {entity}')
        except Exception as e:
            await self._session.rollback()
            logger.exception(f'Ошибка при сохранении пользователя: {entity}')
            raise