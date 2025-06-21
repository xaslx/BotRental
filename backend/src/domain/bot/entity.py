from dataclasses import dataclass, field
from datetime import datetime
from src.domain.user.entity import UserEntity
from src.domain.common.entity import BaseEntity
from src.domain.bot.exception import InvalidLengthException, InvalidPriceException



@dataclass
class BotEntity(BaseEntity):
    name: str
    description: str
    price: int
    is_available: bool = field(default=True)
    is_deleted: bool = field(default=False)
    rentals: list['BotRentalEntity'] = field(default_factory=list)

    @classmethod
    def create_bot(
        cls,
        name: str,
        description: str,
        price: int,
    ) -> 'BotEntity':
        
        if price <= 0:
            raise InvalidPriceException()
        
        if not name or not name.strip():
            raise InvalidLengthException()
        
        if not description or not description.strip():
            raise InvalidLengthException()
        
        return cls(
            name=name,
            description=description,
            price=price,
        )
    
    def deactivate(self):
        self.is_available = False

    def activate(self):
        self.is_available = True

    def delete(self):
        self.is_deleted = True




@dataclass
class BotRentalEntity(BaseEntity):
    user_id: int
    bot_id: int
    token: str
    rented_until: datetime
    is_active: bool = field(default=True, kw_only=True)

    user: UserEntity
    bot: BotEntity