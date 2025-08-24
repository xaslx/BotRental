import logging
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user.entity import UserEntity
from src.domain.user.exception import UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.taskiq.tasks import send_notification_for_admin
from src.presentation.schemas.user import UpdateBalance

logger = logging.getLogger(__name__)


@dataclass
class DepositMoneyForUser:
    _session: AsyncSession
    _user_repository: BaseUserRepository

    async def execute(
        self, telegram_id: int, admin: UserEntity, schema: UpdateBalance
    ) -> bool:
        user: UserEntity | None = await self._user_repository.get_user_by_telegram_id(
            telegram_id=telegram_id
        )
        old_balance: int = user.balance.to_raw()

        if not user:
            raise UserNotFoundException()

        user.deposit(amount=schema.amount)

        await self._user_repository.update(entity=user)
        await self._session.commit()

        logger.info(
            f'Администратор: {admin.telegram_id.to_raw()} увеличил баланс пользователя: {user.telegram_id.to_raw()} ({old_balance} -> {user.balance.to_raw()})',
        )
        await send_notification_for_admin.kiq(
            text=f'Администратор: {admin.telegram_id.to_raw()} увеличил баланс пользователя: {user.telegram_id.to_raw()} ({old_balance} -> {user.balance.to_raw()})'
        )

        return True
