from src.const import MOSCOW_TZ
from src.domain.bot.entity import BotEntity, BotRentalEntity
from src.infrastructure.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.infrastructure.database.models.user import User


class Bot(Base):
    __tablename__ = 'bots'

    name: Mapped[str]
    description: Mapped[str]
    is_available: Mapped[bool]
    is_deleted: Mapped[bool]
    price: Mapped[int]

    rentals: Mapped[list['BotRental']] = relationship(back_populates='bot')

    def to_entity(self) -> BotEntity:
        return BotEntity(
            id=self.id,
            created_at=self.created_at.astimezone(MOSCOW_TZ),
            updated_at=self.updated_at.astimezone(MOSCOW_TZ),
            name=self.name,
            description=self.description,
            is_available=self.is_available,
            is_deleted=self.is_deleted,
            price=self.price,
            rentals=[rental.to_entity() for rental in self.rentals] if self.rentals else [],
    )
    
    @classmethod
    def from_entity(cls, entity: BotEntity) -> 'Bot':
        bot = cls(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            name=entity.name,
            description=entity.description,
            is_available=entity.is_available,
            is_deleted=entity.is_deleted,
            price=entity.price,
        )

        bot.rentals = [BotRental.from_entity(r) for r in entity.rentals]

        return bot



class BotRental(Base):
    __tablename__ = 'bot_rentals'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    bot_id: Mapped[int] = mapped_column(ForeignKey('bots.id'))
    token: Mapped[str]
    rented_until: Mapped[DateTime] = mapped_column(DateTime)
    is_active: Mapped[bool]

    user: Mapped['User'] = relationship(back_populates='rentals')
    bot: Mapped['Bot'] = relationship(back_populates='rentals')

    def to_entity(self) -> BotRentalEntity:
        return BotRentalEntity(
            id=self.id,
            created_at=self.created_at.astimezone(MOSCOW_TZ),
            updated_at=self.updated_at.astimezone(MOSCOW_TZ),
            user_id=self.user_id,
            bot_id=self.bot_id,
            token=self.token,
            rented_until=self.rented_until,
            is_active=self.is_active,
            user=self.user.to_entity() if self.user else None,
            bot=None,
        )

    @classmethod
    def from_entity(cls, entity: BotRentalEntity) -> 'BotRental':
        rental = cls(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_id=entity.user_id,
            bot_id=entity.bot_id,
            token=entity.token,
            rented_until=entity.rented_until,
            is_active=entity.is_active,
        )

        return rental