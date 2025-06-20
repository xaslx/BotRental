from src.domain.user.blocked_user import BlockedUserEntity
from src.infrastructure.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from typing import TYPE_CHECKING
from src.const import MOSCOW_TZ


if TYPE_CHECKING:
    from src.infrastructure.database.models.user import User


class BlockedUser(Base):
    __tablename__ = 'blocked_users'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    blocked_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str]
    blocked_by: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship('User', foreign_keys=[user_id], back_populates='blocks')
    blocker: Mapped['User'] = relationship('User' , foreign_keys=[blocked_by], backref='blocks_made')

    def to_entity(self) -> BlockedUserEntity:
        return BlockedUserEntity(
            id=self.id,
            user_id=self.user_id,
            blocked_until=self.blocked_until.astimezone(MOSCOW_TZ),
            reason=self.reason,
            blocked_by=self.blocked_by,
            created_at=self.created_at.astimezone(MOSCOW_TZ),
            updated_at=self.updated_at.astimezone(MOSCOW_TZ),
        )
    

    @classmethod
    def from_entity(cls, entity: BlockedUserEntity) -> 'BlockedUser':
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            blocked_until=entity.blocked_until,
            reason=entity.reason,
            blocked_by=entity.blocked_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )