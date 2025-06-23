from enum import StrEnum
from dataclasses import dataclass, field
from datetime import datetime
from src.domain.common.entity import BaseEntity
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance
from src.domain.user.blocked_user import BlockedUserEntity
from src.domain.user.exception import (
    AlreadyBlockedException,
    InvalidBlockDurationException,
    ActiveBlockNotFoundException,
)


class Role(StrEnum):
    USER = 'user'
    ADMIN = 'admin'
    DEV = 'dev'


@dataclass
class UserEntity(BaseEntity):
    telegram_id: TelegramId
    balance: Balance = field(default=Balance(value=0))
    is_deleted: bool = field(default=False)
    role: Role = field(default=Role.USER)
    blocks: list[BlockedUserEntity] = field(default_factory=list)

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

    def block(
        self,
        days: int,
        reason: str,
        admin_id: int,
    ) -> BlockedUserEntity:
        
        if self.is_blocked:
            raise AlreadyBlockedException()

        if days is not None and days < 1:
            raise InvalidBlockDurationException()

        block = BlockedUserEntity.create_block(
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
        self.balance.add(amount)

    def withdraw(self, amount: int) -> None:
        self.balance.subtract(amount)

    def delete(self) -> None:
        self.is_deleted = True

    def change_role(self, new_role: Role) -> None:
        self.role = new_role

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
        )
