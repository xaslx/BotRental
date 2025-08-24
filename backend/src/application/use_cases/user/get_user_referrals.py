from dataclasses import dataclass

from src.domain.referral.entity import ReferralEntity
from src.infrastructure.repositories.referral.base import BaseReferralRepository


@dataclass
class GetUserReferralsUseCase:
    _referral_repository: BaseReferralRepository

    async def execute(self, referrer_id: int) -> list[ReferralEntity]:
        return await self._referral_repository.get_all_referrals_by_referrer_id(
            referrer_id=referrer_id,
        )
