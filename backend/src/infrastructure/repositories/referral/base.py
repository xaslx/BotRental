from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.referral.entity import ReferralEntity


@dataclass
class BaseReferralRepository(ABC):
    @abstractmethod
    async def add(self, entity: ReferralEntity) -> ReferralEntity: ...

    @abstractmethod
    async def get_referrals_by_referrer(
        self, referrer_id: int
    ) -> list[ReferralEntity] | None: ...

    @abstractmethod
    async def get_all_referrals_by_referrer_id(
        self, referrer_id: int
    ) -> list[ReferralEntity] | None: ...
