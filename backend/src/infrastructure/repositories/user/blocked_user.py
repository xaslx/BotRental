import logging
from datetime import datetime
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.const import MOSCOW_TZ
from src.domain.user.blocked_user import BlockedUserEntity
from src.infrastructure.database.models.blocked_users import BlockedUser
from dataclasses import dataclass
from src.infrastructure.repositories.user.base import BaseBlockedUserRepository


logger = logging.getLogger(__name__)


@dataclass
class BlockedUserRepository(BaseBlockedUserRepository):

    _session: AsyncSession

    async def add(self, block: BlockedUserEntity) -> None:
        try:
            model: BlockedUser = BlockedUser.from_entity(entity=block)
            self._session.add(model)
            await self._session.commit()
            logger.info(f'Блокировка добавлена для пользователя с id={block.user_id}')
        except Exception as e:
            logger.error(f'Ошибка при добавлении блокировки пользователя id={block.user_id}: {e}')
            raise

    async def update(self, block: BlockedUserEntity) -> None:
        try:
            stmt = select(BlockedUser).where(BlockedUser.id == block.id)
            result = await self._session.execute(stmt)
            db_block = result.scalar_one_or_none()

            if db_block is None:
                msg = f'Блокировка с id={block.id} не найдена для обновления'
                logger.warning(msg)
                raise Exception(msg)

            db_block.blocked_until = block.blocked_until
            db_block.reason = block.reason
            db_block.blocked_by = block.blocked_by

            await self._session.commit()
            logger.info(f'Блокировка с id={block.id} успешно обновлена')
        except Exception as e:
            logger.error(f'Ошибка при обновлении блокировки id={block.id}: {e}')
            raise

    async def get_active_block_by_user_id(self, user_id: int) -> BlockedUserEntity | None:
        try:
            now: datetime = datetime.now(tz=MOSCOW_TZ)
            stmt = select(BlockedUser).where(
                BlockedUser.user_id == user_id,
                or_(
                    BlockedUser.blocked_until == None,
                    BlockedUser.blocked_until > now
                )
            )
            result = await self._session.execute(stmt)
            db_block = result.scalar_one_or_none()
            if db_block is None:
                logger.info(f'Активная блокировка для пользователя id={user_id} не найдена')
                return None
            return db_block.to_entity()
        except Exception as e:
            raise

    async def get_all_by_user_id(self, user_id: int) -> list[BlockedUserEntity]:
        try:
            stmt = select(BlockedUser).where(BlockedUser.user_id == user_id)
            result = await self._session.execute(stmt)
            db_blocks = result.scalars().all()
            logger.info(f'Найдено {len(db_blocks)} блокировок для пользователя id={user_id}')
            return [db_block.to_entity() for db_block in db_blocks]
        except Exception as e:
            logger.error(f'Ошибка при получении всех блокировок пользователя id={user_id}: {e}')
            raise
