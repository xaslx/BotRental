from functools import wraps
from typing import Callable, TypeVar, Any
from fastapi import HTTPException, status
from src.domain.common.exception import ApplicationException
import logging


logger = logging.getLogger(__name__)


T = TypeVar('T')


def handle_exceptions(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except ApplicationException as e:
            logger.error(f'Ошибка приложения: {e}')
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Internal server error'
            )
    return wrapper