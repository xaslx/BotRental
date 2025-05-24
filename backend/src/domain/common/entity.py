from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import datetime as dt
from src.const import MOSCOW_TZ


@dataclass(kw_only=True)
class BaseEntity(ABC):

    id: int | None = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=MOSCOW_TZ))
    updated_at: datetime = field(default_factory=lambda: datetime.now(tz=MOSCOW_TZ))
    
    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id