from dataclasses import dataclass

from fastapi import status
from src.domain.common.exception import DomainErrorException


@dataclass(eq=False)
class UserAlreadyExistsException(DomainErrorException):
    status_code: int = status.HTTP_409_CONFLICT

    @property
    def message(self) -> str:
        return 'Пользователь уже существует.'


@dataclass(eq=False)
class NotEnoughBalanceError(DomainErrorException):
    status_code: int = status.HTTP_402_PAYMENT_REQUIRED

    @property
    def message(self) -> str:
        return 'Недостаточно средств.'


@dataclass(eq=False)
class UserNotFoundException(DomainErrorException):
    status_code: int = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Пользователь не найден.'


@dataclass(eq=False)
class PermissionDeniedException(DomainErrorException):
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
        return 'Код уже был отправлен, попробуйте через 5 минут.'


@dataclass(eq=False)
class InvalidBlockDurationException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Количество дней должно быть больше 1.'


@dataclass(eq=False)
class AlreadyBlockedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Пользователь уже заблокирован.'


@dataclass(eq=False)
class ActiveBlockNotFoundException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Активная блокировка не найдена.'


@dataclass(eq=False)
class SelfBlockException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Администратор не может заблокировать самого себя.'


@dataclass(eq=False)
class ReferrerAlreadyAssignedException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Реферер уже назначен для этого пользователя.'


@dataclass(eq=False)
class ReferrerNotFoundException(DomainErrorException):
    status_code: int = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Пригласивший пользователь не найден.'


@dataclass(eq=False)
class SelfReferralException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Пользователь не может пригласить сам себя.'


@dataclass(eq=False)
class DuplicateReferralException(DomainErrorException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Этот пользователь уже был добавлен как реферал.'
