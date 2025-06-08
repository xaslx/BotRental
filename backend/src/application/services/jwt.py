from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from src.domain.jwt.exception import IncorrectTokenException, TokenExpiredException
from src.config import Config
from jose import ExpiredSignatureError, JWTError, jwt
from dataclasses import dataclass
from src.const import MOSCOW_TZ
from fastapi import HTTPException, status


@dataclass
class JWTService(ABC):
    
    @abstractmethod
    def _create_access_token(self, data: dict, exp: int | None = None) -> str:
        ...

    @abstractmethod
    def _create_refresh_token(self, data: dict, exp: int | None = None) -> str:
        ...

    @abstractmethod
    def create_tokens(self, data: dict, exp: int | None = None) -> tuple[str, str]:
        ...

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> dict:
        ...
        
    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> str:
        ...


@dataclass   
class JWTServiceImpl(JWTService):
    config: Config

    def _create_token(
        self, 
        data: dict, 
        expires_delta: timedelta,
        token_type: str,
        secret_key: str
    ) -> str:

        to_encode = data.copy()
        expire = datetime.now(tz=MOSCOW_TZ) + expires_delta
        to_encode.update({'exp': expire, 'type': token_type})
        return jwt.encode(
            to_encode, 
            secret_key, 
            algorithm=self.config.jwt.algorithm
        )

    def _verify_token(
        self,
        token: str,
        expected_type: str,
        secret_key: str
    ) -> dict:

        try:
            payload = jwt.decode(
                token, 
                secret_key, 
                algorithms=[self.config.jwt.algorithm]
            )
            if payload.get('type') != expected_type:
                raise IncorrectTokenException('Invalid token type')
            return payload
        except ExpiredSignatureError:
            raise TokenExpiredException()
        except JWTError:
            raise IncorrectTokenException()

    def _create_access_token(self, data: dict, exp: int | None = None) -> str:
        expires_delta = timedelta(
            minutes=exp or self.config.jwt.access_token_expire_minutes
        )
        return self._create_token(
            data, 
            expires_delta, 
            'access',
            self.config.jwt.secret_key,
        )

    def _create_refresh_token(self, data: dict, exp: int | None = None) -> str:
        expires_delta = timedelta(
            days=exp or self.config.jwt.refresh_token_expire_days
        )
        return self._create_token(
            data, 
            expires_delta, 
            'refresh',
            self.config.jwt.refresh_secret_key,
        )
    
    def create_tokens(self, data: dict, exp: int | None = None) -> tuple[str, str]:
        access_token: str = self._create_access_token(data=data, exp=exp)
        refresh_token: str = self._create_refresh_token(data=data, exp=exp)
        return access_token, refresh_token

    def verify_access_token(self, token: str) -> dict:
        return self._verify_token(
            token,
            'access',
            self.config.jwt.secret_key,
        )

    def verify_refresh_token(self, token: str) -> dict:
        return self._verify_token(
            token,
            'refresh',
            self.config.jwt.refresh_secret_key,
        )
        
    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = self.verify_refresh_token(refresh_token)
            payload.pop('exp', None)
            payload.pop('type', None)
            
            return self._create_access_token(payload)
        except (TokenExpiredException, IncorrectTokenException) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
            )
