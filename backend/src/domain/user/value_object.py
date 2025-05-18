from dataclasses import dataclass
from src.domain.common.value_object import BaseValueObject
from src.domain.user.exception import InvalidTelegramIDTypeError, InvalidTelegramIDValueError



@dataclass(frozen=True)
class TelegramId(BaseValueObject):

    def validate(self):

        if not isinstance(self.value, int):
            raise InvalidTelegramIDTypeError()
        if self.value <= 0:
            raise InvalidTelegramIDValueError()

    def __eq__(self, value: 'TelegramId') -> bool:
        if not isinstance(value, TelegramId):
            return False
        return self.value == value.value

    def to_raw(self):
        return self.value