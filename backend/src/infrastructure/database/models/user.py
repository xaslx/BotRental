from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.const import MOSCOW_TZ
from src.domain.balance.value_object import Balance
from src.domain.user.entity import Role, UserEntity
from src.domain.user.value_object import TelegramId
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.blocked_users import BlockedUser
from src.infrastructure.database.models.bots import BotRental
from src.infrastructure.database.models.referrals import Referral


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger)
    is_deleted: Mapped[bool]
    balance: Mapped[int]
    role: Mapped[Role] = mapped_column(
        SQLEnum(
            Role,
            name='user_role_enum',
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj],
        )
    )
    referrer_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id'), nullable=True
    )
    total_bonus_received: Mapped[int]

    rentals: Mapped[list['BotRental']] = relationship(
        back_populates='user', lazy='selectin', cascade='all, delete-orphan'
    )

    blocks: Mapped[list['BlockedUser']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        foreign_keys='BlockedUser.user_id',
        lazy='selectin',
    )

    referrals: Mapped[list['Referral']] = relationship(
        back_populates='referrer',
        cascade='all, delete-orphan',
        foreign_keys='Referral.referrer_id',
        lazy='selectin',
    )

    referred_by: Mapped['Referral | None'] = relationship(
        back_populates='referral',
        uselist=False,
        foreign_keys='Referral.referral_id',
        lazy='selectin',
    )

    def to_entity(self, include_relations: bool = True) -> UserEntity:
        return UserEntity(
            id=self.id,
            created_at=self.created_at.astimezone(MOSCOW_TZ),
            updated_at=self.updated_at.astimezone(MOSCOW_TZ),
            telegram_id=TelegramId(value=self.telegram_id),
            is_deleted=self.is_deleted,
            balance=Balance(value=self.balance),
            role=self.role,
            blocks=[block.to_entity() for block in self.blocks]
            if include_relations
            else [],
            referrer_id=self.referrer_id,
            total_bonus_received=self.total_bonus_received,
            rentals=[rental.to_entity(include_user=False) for rental in self.rentals]
            if include_relations
            else [],
            referrals=[ref.to_entity() for ref in self.referrals]
            if include_relations
            else [],
        )

    @classmethod
    def from_entity(cls, entity: UserEntity) -> 'User':
        user = cls(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            telegram_id=entity.telegram_id.to_raw(),
            is_deleted=entity.is_deleted,
            balance=entity.balance.to_raw(),
            role=entity.role,
            referrer_id=entity.referrer_id,
            total_bonus_received=entity.total_bonus_received,
        )

        user.blocks = [BlockedUser.from_entity(block) for block in entity.blocks]

        return user
