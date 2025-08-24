from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from src.domain.balance.value_object import Balance
from src.domain.bot.entity import BotRentalEntity
from src.domain.common.entity import BaseEntity
from src.domain.referral.entity import ReferralEntity
from src.domain.user.blocked_user import BlockedUserEntity
from src.domain.user.exception import (
    ActiveBlockNotFoundException,
    AlreadyBlockedException,
    InvalidBlockDurationException,
    ReferrerAlreadyAssignedException,
    SelfReferralException,
)
from src.domain.user.value_object import TelegramId


class Role(StrEnum):
    USER = 'user'
    ADMIN = 'admin'
    DEV = 'dev'


BONUS_AMOUNT: int = 50
WELCOME_BONUS: int = 100


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    telegram_id: TelegramId
    balance: Balance = field(default=Balance(value=0))
    is_deleted: bool = field(default=False)
    role: Role = field(default=Role.USER)
    blocks: list[BlockedUserEntity] = field(default_factory=list)
    referrer_id: int | None = field(default=None)
    total_bonus_received: int = field(default=0)
    rentals: list[BotRentalEntity] = field(default_factory=list)
    referrals: list[ReferralEntity] = field(default_factory=list)

    def add_welcome_bonus(self) -> None:
        self.deposit(amount=WELCOME_BONUS)

    @classmethod
    def create_user(cls, telegram_id: int) -> 'UserEntity':
        return cls(telegram_id=TelegramId(value=telegram_id))

    @property
    def is_blocked(self) -> bool:
        now = datetime.now(tz=self.created_at.tzinfo)
        return any(
            block.blocked_until is None or block.blocked_until > now
            for block in self.blocks
        )

    def add_rental(self, rental: BotRentalEntity) -> None:
        self.rentals.append(rental)

    def block(self, days: int, reason: str, admin_id: int) -> BlockedUserEntity:
        if self.is_blocked:
            raise AlreadyBlockedException()

        if days is not None and days < 1:
            raise InvalidBlockDurationException()

        block: BlockedUserEntity = BlockedUserEntity.create_block(
            user_id=self.id,
            days=days,
            reason=reason,
            blocked_by=admin_id,
        )
        self.blocks.append(block)
        return block

    def unblock(self) -> BlockedUserEntity:
        now = datetime.now(tz=self.created_at.tzinfo)

        for block in self.blocks:
            if block.blocked_until is None or block.blocked_until > now:
                block.unblock()
                return block

        raise ActiveBlockNotFoundException()

    def deposit(self, amount: int) -> None:
        self.balance = self.balance.add(amount)

    def withdraw(self, amount: int) -> None:
        self.balance = self.balance.subtract(amount)

    def delete(self) -> None:
        self.is_deleted = True

    def change_role(self, new_role: Role) -> None:
        self.role = new_role

    def assign_referrer(self, referrer_id: int) -> None:
        if self.referrer_id:
            raise ReferrerAlreadyAssignedException()
        if referrer_id == self.id:
            raise SelfReferralException()
        self.referrer_id = referrer_id

    def add_referral_bonus(self) -> None:
        self.deposit(BONUS_AMOUNT)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'telegram_id': self.telegram_id.to_raw(),
            'balance': self.balance.to_raw(),
            'is_deleted': self.is_deleted,
            'role': self.role.value,
            'blocks': [block.to_dict() for block in self.blocks],
            'rentals': [rental.to_dict() for rental in self.rentals],
            'referrals': [ref.to_dict() for ref in self.referrals],
            'referrer_id': self.referrer_id,
            'total_bonus_received': self.total_bonus_received,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'UserEntity':
        return cls(
            id=data['id'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            telegram_id=TelegramId(data['telegram_id']),
            balance=Balance(data['balance']),
            is_deleted=data['is_deleted'],
            role=Role(data['role']),
            blocks=[BlockedUserEntity.from_dict(b) for b in data.get('blocks', [])],
            rentals=[BotRentalEntity.from_dict(r) for r in data.get('rentals', [])],
            referrals=[ReferralEntity.from_dict(r) for r in data.get('referrals', [])],
            referrer_id=data.get('referrer_id'),
            total_bonus_received=data.get('total_bonus_received', 0),
        )
