from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.infrastructure.repositories.referral.base import BaseReferralRepository
from src.domain.referral.entity import ReferralEntity
from src.infrastructure.database.models.referrals import Referral
import logging
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


@dataclass
class SQLAlchemyReferralRepository(BaseReferralRepository):

    _session: AsyncSession

    async def add(self, entity: ReferralEntity) -> ReferralEntity:
        try:
            model: Referral = Referral.from_entity(entity=entity)
            self._session.add(model)
            await self._session.commit()
            logger.info(f'Реферал добавлен: {entity}')
            return model.to_entity()
        except Exception as e:
            logger.exception(f'Ошибка при добавлении реферала: {entity} в БД')
            raise

    async def get_referrals_by_referrer(self, referrer_id: int) -> list[ReferralEntity]:
        result = await self._session.execute(
            select(Referral)
            .where(Referral.referrer_id == referrer_id)
            .options(selectinload(Referral.referral))
        )
        referrals = result.scalars().all()
        return [ref.to_entity() for ref in referrals]
