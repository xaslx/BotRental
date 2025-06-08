from sqlalchemy.orm import mapped_column, Mapped
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.base import Base
from src.domain.user.value_object import TelegramId
from src.domain.balance.value_object import Balance


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int]
    is_active: Mapped[bool]
    is_deleted: Mapped[bool]
    balance: Mapped[int]

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            telegram_id=TelegramId(value=self.telegram_id),
            is_active=self.is_active,
            is_deleted=self.is_deleted,
            balance=Balance(value=self.balance),
        )
    
    @classmethod
    def from_entity(cls, entity: UserEntity) -> 'User':
        return cls(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            telegram_id=entity.telegram_id.to_raw(),
            is_active=entity.is_active,
            is_deleted=entity.is_deleted,
            balance=entity.balance.to_raw(),
        )