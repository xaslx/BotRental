from dataclasses import dataclass
from src.domain.common.value_object import BaseValueObject
from src.domain.bot.exception import InvalidLengthException, InvalidPriceException


@dataclass(frozen=True)
class BotName(BaseValueObject[str]):
    def validate(self):
        if not self.value or not self.value.strip():
            raise InvalidLengthException()

    def to_raw(self) -> str:
        return self.value


@dataclass(frozen=True)
class BotDescription(BaseValueObject[str]):
    def validate(self):
        if not self.value or not self.value.strip():
            raise InvalidLengthException()

    def to_raw(self) -> str:
        return self.value


@dataclass(frozen=True)
class BotPrice(BaseValueObject[int]):
    def validate(self):
        if self.value <= 0:
            raise InvalidPriceException()

    def to_raw(self) -> int:
        return self.value
