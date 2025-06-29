from dataclasses import dataclass, field
from datetime import datetime
from src.const import MOSCOW_TZ
from src.domain.common.entity import BaseEntity


@dataclass
class ReferralEntity(BaseEntity):
    referrer_id: int
    referral_id: int
    telegram_id: int
    invited_at: datetime = field(default_factory=lambda: datetime.now(tz=MOSCOW_TZ))
    total_bonus: int = field(default=0)

    def add_bonus(self, amount: int) -> None:
        self.total_bonus += amount

    @classmethod
    def create_referral(
        cls,
        referrer_id: int,
        referral_id: int,
        telegram_id: int,
    ) -> 'ReferralEntity':
        
        return cls(
            referrer_id=referrer_id,
            referral_id=referral_id,
            telegram_id=telegram_id,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'referrer_id': self.referrer_id,
            'referral_id': self.referral_id,
            'telegram_id': self.telegram_id,
            'invited_at': self.invited_at.isoformat(),
            'total_bonus': self.total_bonus,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ReferralEntity':
        return cls(
            id=data.get('id'),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            referrer_id=data['referrer_id'],
            referral_id=data['referral_id'],
            telegram_id=data['telegram_id'],
            invited_at=datetime.fromisoformat(data['invited_at']),
            total_bonus=data.get('total_bonus', 0),
        )
