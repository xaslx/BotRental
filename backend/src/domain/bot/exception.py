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