from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.database.models.bots import BotRental
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.base import Base
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance
from sqlalchemy import Enum as SQLEnum, BigInteger
from src.domain.user.entity import Role
from src.infrastructure.database.models.blocked_users import BlockedUser
from src.const import MOSCOW_TZ


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger)
    is_deleted: Mapped[bool]
    balance: Mapped[int]
    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name='user_role_enum', native_enum=False, values_callable=lambda obj: [e.value for e in obj])
    )

    rentals: Mapped[list['BotRental']] = relationship(back_populates='user')
    blocks: Mapped[list['BlockedUser']] = relationship(
        back_populates="user",
        cascade='all, delete-orphan',
        foreign_keys='BlockedUser.user_id',
        lazy='selectin'
    )


    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            created_at=self.created_at.astimezone(MOSCOW_TZ),
            updated_at=self.updated_at.astimezone(MOSCOW_TZ),
            telegram_id=TelegramId(value=self.telegram_id),
            is_deleted=self.is_deleted,
            balance=Balance(value=self.balance),
            role=self.role,
            blocks=[block.to_entity() for block in self.blocks],
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
        )

        user.blocks = [BlockedUser.from_entity(block) for block in entity.blocks]

        return user