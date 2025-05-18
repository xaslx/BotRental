from dishka import Provider, Scope, provide, from_context
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable
from src.config import Config
from src.infrastructure.database.postgresql import new_session_maker
from src.application.use_cases.user.register import NewUserUseCase, RegisterUserUseCase
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.repositories.user.sqlalchemy import SQLAlchemyUserRepository
from src.infrastructure.cache.base import BaseCacheService
from src.infrastructure.cache.redis import RedisCacheService
from src.application.services.code import CheckCodeService, SendCodeService


class AppProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)


    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


    #REPOSITORIES
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(_session=session)


    #USE CASES
    @provide(scope=Scope.REQUEST)
    def get_new_user_use_case(
        self,
        cache_service: BaseCacheService,
        send_code_service: SendCodeService,
        user_repository: BaseUserRepository,
    ) -> NewUserUseCase:
        
        return NewUserUseCase(
            user_repository=user_repository,
            send_code_service=send_code_service,
            cache_service=cache_service,
        )

    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(
        self,
        check_code: CheckCodeService,
        user_repository: BaseUserRepository,
    ) -> RegisterUserUseCase:
        
        return RegisterUserUseCase(
            check_code=check_code,
            user_repository=user_repository,
        )

    #SERVICES
    @provide(scope=Scope.REQUEST)
    def get_cache_service(
        self,
    ) -> BaseCacheService:
        
        return RedisCacheService()
    
    @provide(scope=Scope.REQUEST)
    def get_send_code_service(
        self,
        user_repository: BaseUserRepository,
        cache_service: BaseCacheService,
    ) -> SendCodeService:
        
        return SendCodeService(user_repository=user_repository, cache_service=cache_service)
        
    @provide(scope=Scope.REQUEST)
    def get_check_code_service(
        self,
        cache_service: BaseCacheService,
    ) -> CheckCodeService:
        
        return CheckCodeService(
            cache_service=cache_service,
        )

    # #current user
    # @provide(scope=Scope.REQUEST)
    # def get_token(self, request: Request) -> str:
        
    #     token: str = request.cookies.get('user_access_token')
    
    #     if not token:
    #         return None
    #     return token


    # @provide(scope=Scope.REQUEST)
    # async def get_current_user_dependency(
    #     self,
    #     auth_service: BaseAuthService,
    #     token: str,
    # ) -> UserEntity:

    #     if not token:
    #         return None
        
    #     return await auth_service.get_current_user(token=token)