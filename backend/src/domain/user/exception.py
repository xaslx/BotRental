from src.domain.common.exception import DomainErrorException
from fastapi import status
from dataclasses import dataclass


@dataclass(eq=False)
class UserAlreadyExistsException(DomainErrorException):
    status_code: int = status.HTTP_409_CONFLICT

    @property
    def message(self) -> str:
        return 'Пользователь уже существует.'


@dataclass(eq=False)
class UserNotFoundException(DomainErrorException):
    status_code: int = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Пользователь не найден.'


@dataclass(eq=False)
class NotAccessErrorException(DomainErrorException):
    status_code: int = status.HTTP_403_FORBIDDEN 

    @property
    def message(self) -> str:
        return 'Недостаточно прав.'

@dataclass(eq=False)
class UserIsNotPresentException(DomainErrorException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'Требуется аутентификация.'


@dataclass(eq=False)
class UserNotAuthenticatedException(DomainErrorException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'Пользователь не аутентифицирован.'
    


@dataclass(eq=False)
class InvalidTelegramIDTypeException(DomainErrorException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

    @property
    def message(self) -> str:
        return 'Telegram ID должен быть в виде целого числа.'

@dataclass(eq=False)
class InvalidTelegramIDValueException(DomainErrorException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

    @property
    def message(self) -> str:
        return 'Telegram ID должен быть больше 0.'
    

@dataclass(eq=False)
class InvalidCodeException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Неверный код. Попробуйте еще раз.'
    

@dataclass(eq=False)
class TooManyCodeRequestsException(DomainErrorException):
    status_code: int = status.HTTP_429_TOO_MANY_REQUESTS
    
    @property
    def message(self) -> str:
        return 'Код уже был отправлен, попробуйте через 5 минут'