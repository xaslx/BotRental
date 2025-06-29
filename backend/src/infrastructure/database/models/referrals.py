from sqlalchemy import ForeignKey, DateTime, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.infrastructure.database.models.base import Base
from src.domain.referral.entity import ReferralEntity
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from src.infrastructure.database.models.user import User




class Referral(Base):
    __tablename__ = 'referrals'

    referrer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    referral_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    invited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    total_bonus: Mapped[int]

    __table_args__ = (
        UniqueConstraint('referrer_id', 'referral_id', name='uq_referrer_referral'),
    )

    referrer: Mapped['User'] = relationship(
        foreign_keys=[referrer_id],
        back_populates='referrals',
    )

    referral: Mapped['User'] = relationship(
        foreign_keys=[referral_id],
        back_populates='referred_by',
    )

    @classmethod
    def from_entity(cls, entity: ReferralEntity) -> 'Referral':
        return cls(
            referrer_id=entity.referrer_id,
            referral_id=entity.referral_id,
            invited_at=entity.invited_at,
            telegram_id=entity.telegram_id,
            total_bonus=entity.total_bonus,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> ReferralEntity:
        return ReferralEntity(
            referrer_id=self.referrer_id,
            referral_id=self.referral_id,
            telegram_id=self.telegram_id,
            invited_at=self.invited_at,
            total_bonus=self.total_bonus,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
