from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.const import MOSCOW_TZ
from src.infrastructure.database.models.base import Base


def moscow_now():
    return datetime.now(MOSCOW_TZ)


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=moscow_now
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=moscow_now,
        onupdate=moscow_now,
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger())

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
