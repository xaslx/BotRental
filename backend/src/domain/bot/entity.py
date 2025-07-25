from dataclasses import dataclass, field
from datetime import datetime
from src.domain.common.entity import BaseEntity
from src.domain.bot.exception import BotAlreadyDeletedException, BotAlreadyActivatedException, BotAlreadyDeactivatedException
from src.domain.bot.value_object import BotName, BotPrice, BotDescription
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.user.entity import UserEntity

@dataclass
class BotEntity(BaseEntity):
    name: BotName
    description: BotDescription
    price: BotPrice
    is_available: bool = field(default=True)
    is_deleted: bool = field(default=False)
    rentals: list['BotRentalEntity'] = field(default_factory=list)

    @classmethod
    def create_bot(cls, name: str, description: str, price: int) -> 'BotEntity':
        return cls(
            name=BotName(value=name),
            description=BotDescription(value=description),
            price=BotPrice(value=price),
        )

    def update(
            self, *, 
            name: str | None = None,
            description: str | None = None,
            price: int | None = None,
            is_available: bool | None = None,
        ):

        if name is not None:
            self.name = BotName(value=name)

        if description is not None:
            self.description = BotDescription(value=description)

        if price is not None:
            self.price = BotPrice(value=price)

        if is_available is not None:
            self.is_available = is_available

    def deactivate(self):
        if not self.is_available:
            raise BotAlreadyDeactivatedException()
        self.is_available = False

    def activate(self):
        if self.is_available:
            raise BotAlreadyActivatedException()
        self.is_available = True

    def delete(self):
        if self.is_deleted:
            raise BotAlreadyDeletedException()
        self.is_deleted = True
        self.is_available = False

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'name': self.name.to_raw(),
            'description': self.description.to_raw(),
            'price': self.price.to_raw(),
            'is_available': self.is_available,
            'is_deleted': self.is_deleted,
            'rentals': [rental.to_dict() for rental in self.rentals] if self.rentals else [],
        }


@dataclass
class BotRentalEntity(BaseEntity):
    user_id: int
    bot_id: int
    token: str
    rented_until: datetime
    is_active: bool = field(default=True, kw_only=True)

    user: 'UserEntity'
    bot: BotEntity

    @classmethod
    def from_dict(cls, data: dict) -> 'BotRentalEntity':
        from src.domain.user.entity import UserEntity
        from src.domain.bot.entity import BotEntity

        return cls(
            id=data.get('id'),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            user_id=data['user_id'],
            bot_id=data['bot_id'],
            token=data['token'],
            rented_until=datetime.fromisoformat(data['rented_until']) if data.get('rented_until') else None,
            is_active=data.get('is_active', True),
            user=UserEntity.from_dict(data['user']) if data.get('user') else None,
            bot=BotEntity.from_dict(data['bot']) if data.get('bot') else None,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'bot_id': self.bot_id,
            'token': self.token,
            'rented_until': self.rented_until.isoformat() if self.rented_until else None,
            'is_active': self.is_active,
            'user': self.user.to_dict() if self.user else None,
            'bot': self.bot.to_dict() if self.bot else None,
        }
