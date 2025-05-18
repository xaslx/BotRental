from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity(ABC):

    id: int | None = None
    created_at: datetime | None = None
    
    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id