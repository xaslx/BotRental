from dataclasses import dataclass

from src.domain.common.value_object import BaseValueObject
from src.domain.user.exception import (
    InvalidTelegramIDTypeException,
    InvalidTelegramIDValueException,
)


@dataclass(frozen=True)
class TelegramId(BaseValueObject[int]):
    def validate(self):
        if not isinstance(self.value, int):
            raise InvalidTelegramIDTypeException()
        if self.value <= 0:
            raise InvalidTelegramIDValueException()

    def to_raw(self):
        return self.value
