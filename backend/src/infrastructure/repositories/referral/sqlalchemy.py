import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.domain.referral.entity import ReferralEntity
from src.infrastructure.database.models.referrals import Referral
from src.infrastructure.repositories.referral.base import BaseReferralRepository

logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyReferralRepository(BaseReferralRepository):
    _session: AsyncSession

    async def add(self, entity: ReferralEntity) -> ReferralEntity:
        try:
            model = Referral.from_entity(entity)
            self._session.add(model)
            logger.info(f'Реферал добавлен: {entity}')
            return entity
        except Exception:
            logger.exception(f'Ошибка при добавлении реферала: {entity}')
            raise

    async def get_referrals_by_referrer(self, referrer_id: int) -> list[ReferralEntity]:
        try:
            result = await self._session.execute(
                select(Referral)
                .where(Referral.referrer_id == referrer_id)
                .options(selectinload(Referral.referral))
            )
            referrals = result.scalars().all()
            logger.info(
                f'Найдено {len(referrals)} рефералов по referrer_id={referrer_id}'
            )
            return [ref.to_entity() for ref in referrals]
        except Exception:
            logger.exception(
                f'Ошибка при получении рефералов по referrer_id={referrer_id}'
            )
            return []

    async def get_all_referrals_by_referrer_id(
        self, referrer_id: int
    ) -> list[ReferralEntity]:
        try:
            result = await self._session.execute(
                select(Referral).where(Referral.referrer_id == referrer_id)
            )
            referrals = result.scalars().all()
            logger.info(
                f'Найдено {len(referrals)} рефералов по referrer_id={referrer_id}'
            )
            return [ref.to_entity() for ref in referrals]
        except Exception:
            logger.exception(
                f'Ошибка при получении всех рефералов по referrer_id={referrer_id}'
            )
            return []
