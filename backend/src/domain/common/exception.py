from dataclasses import dataclass
from fastapi import HTTPException, status


@dataclass(eq=False)
class ApplicationException(Exception):
    status_code: int

    @property
    def message(self) -> str:
        return 'Произошла ошибка приложения.'
    
@dataclass(eq=False)
class DomainErrorException(ApplicationException):
    ...