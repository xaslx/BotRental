from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.infrastructure.repositories.telegram.base import BaseTelegramRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.telegram_users import TelegramUser
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

@dataclass
class SQLAlchemyTelegramRepository(BaseTelegramRepository):
    _session: AsyncSession

    async def add_user_if_not_exists(self, telegram_id: int) -> TelegramUser:
        try:
            result = await self._session.execute(
                select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            if user is None:
                user = TelegramUser(telegram_id=telegram_id)
                self._session.add(user)
                await self._session.commit()
                await self._session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Ошибка при добавлении пользователя с telegram_id={telegram_id}: {e}")


    async def get_all_users(self) -> list[TelegramUser]:
        try:
            result = await self._session.execute(select(TelegramUser))
            users = result.scalars().all()
            return users
        except Exception as e:
            logger.error(f"Ошибка при получении списка пользователей: {e}")
            return []

