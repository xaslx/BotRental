from dataclasses import dataclass

from fastapi import status
from src.domain.common.exception import DomainErrorException


@dataclass(eq=False)
class TokenExpiredException(DomainErrorException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'JWT токен устарел.'


@dataclass(eq=False)
class TokenAbsentException(DomainErrorException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'Токен отсутствует.'


@dataclass(eq=False)
class IncorrectTokenException(DomainErrorException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'Неверный формат токена.'
