from enum import StrEnum
from src.domain.common.entity import BaseEntity
from dataclasses import dataclass, field
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance




class Role(StrEnum):
    USER = 'user'
    ADMIN = 'admin'


@dataclass
class UserEntity(BaseEntity):
    telegram_id: TelegramId
    balance: Balance = field(default=Balance(value=0))
    is_active: bool = field(default=True)
    is_deleted: bool = field(default=False)
    role: Role = field(default=Role.USER)

    @classmethod
    def create_user(
        cls,
        telegram_id: int,
    ) -> 'UserEntity':
        
        return cls(telegram_id=TelegramId(value=telegram_id))
    
    def deposit(self, amount: int) -> None:
        self.balance.add(amount=amount)

    def withdraw(self, amount: int) -> None:
        self.balance.subtract(amount=amount)

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def delete(self) -> None:
        self.is_deleted = True