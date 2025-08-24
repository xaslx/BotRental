from dataclasses import dataclass
from datetime import datetime, timedelta

from src.const import MOSCOW_TZ
from src.domain.common.entity import BaseEntity
from src.domain.user.exception import InvalidBlockDurationException


@dataclass
class BlockedUserEntity(BaseEntity):
    user_id: int
    blocked_until: datetime
    reason: str
    blocked_by: int

    @property
    def is_active(self) -> bool:
        now = datetime.now(tz=self.blocked_until.tzinfo)
        return self.blocked_until is None or self.blocked_until > now

    @classmethod
    def create_block(
        cls,
        user_id: int,
        days: int,
        reason: str,
        blocked_by: int,
    ) -> 'BlockedUserEntity':
        if days < 1:
            raise InvalidBlockDurationException()

        now = datetime.now(tz=MOSCOW_TZ)
        blocked_until = now + timedelta(days=days)

        return cls(
            user_id=user_id,
            blocked_until=blocked_until,
            reason=reason,
            blocked_by=blocked_by,
        )

    def unblock(self) -> None:
        if not self.is_active:
            return
        self.blocked_until = datetime.now(tz=self.blocked_until.tzinfo)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'blocked_until': self.blocked_until.isoformat()
            if self.blocked_until
            else None,
            'reason': self.reason,
            'blocked_by': self.blocked_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BlockedUserEntity':
        return cls(
            id=data.get('id'),
            user_id=data['user_id'],
            blocked_until=datetime.fromisoformat(data['blocked_until'])
            if data.get('blocked_until')
            else None,
            reason=data.get('reason'),
            blocked_by=data.get('blocked_by'),
            created_at=datetime.fromisoformat(data['created_at'])
            if data.get('created_at')
            else None,
            updated_at=datetime.fromisoformat(data['updated_at'])
            if data.get('updated_at')
            else None,
        )
