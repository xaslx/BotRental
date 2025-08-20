from src.domain.common.exception import DomainErrorException
from dataclasses import dataclass
from fastapi import status


@dataclass(eq=False)
class InvalidPriceException(DomainErrorException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

    @property
    def message(self) -> str:
        return 'Цена должна быть больше 0.'
    
    
@dataclass(eq=False)
class InvalidLengthException(DomainErrorException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

    @property
    def message(self) -> str:
        return 'Поле не должно быть пустым.'
    

@dataclass(eq=False)
class BotNotFoundException(DomainErrorException):
    status_code: int = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Бот не найден.'
    
@dataclass(eq=False)
class BotCannotBeRentedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Бота сейчас нельзя арендовать.'
    

@dataclass(eq=False)
class BotAlreadyDeletedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Бот уже удален.'
    

@dataclass(eq=False)
class BotAlreadyActivatedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Бот уже активирован.'
    

@dataclass(eq=False)
class BotAlreadyDeactivatedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Бот уже деактивирован.'
    

@dataclass(eq=False)
class RentalAlreadyStoppedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Аренда бота уже остановлена.'


@dataclass(eq=False)
class RentalAlreadyActiveException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Аренда бота уже активна.'