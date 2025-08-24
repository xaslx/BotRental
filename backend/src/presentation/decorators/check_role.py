from functools import wraps

from src.domain.user.entity import UserEntity
from src.domain.user.exception import PermissionDeniedException


def check_role(allowed_roles: list[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: UserEntity | None = kwargs.get('user')

            if not user or user.role not in allowed_roles:
                raise PermissionDeniedException()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
