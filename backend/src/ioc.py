from dishka import Provider, Scope, provide, from_context
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable
from src.application.use_cases.admin.bot.change_status_bot import DeactivateBotUseCase, ActivateBotUseCase
from src.application.use_cases.admin.bot.update_bot import UpdateBotUseCase
from src.application.use_cases.admin.bot.delete_bot import DeleteBotUseCase
from src.application.use_cases.admin.bot.get_all_bots_with_rentals import GetAllBotsWithRentalsUseCase
from src.application.use_cases.user.bot.get_all_bots import GetAllBotsUseCase
from src.application.use_cases.admin.bot.create_bot import CreateNewBotUseCase
from src.infrastructure.repositories.bot.base import BaseBotRepository
from src.infrastructure.repositories.bot.sqlalchemy import SQLAlchemyBotRepository
from src.application.use_cases.admin.users.unblock_user import UnblockUserUseCase
from src.application.use_cases.admin.users.block_user import BlockUserUseCase
from src.application.use_cases.admin.users.update_role import UpdateUserRoleUseCase
from src.application.use_cases.admin.users.delete_user import DeleteUserUseCase
from src.application.use_cases.admin.users.get_users import GetAllUsersUseCase, GetUserByTelegramId
from src.domain.user.entity import UserEntity
from src.application.services.auth import AuthServiceImpl, BaseAuthService
from src.application.services.jwt import JWTService, JWTServiceImpl
from src.config import Config
from src.infrastructure.database.postgresql import new_session_maker
from src.application.use_cases.user.auth import RefreshTokenUseCase, RegisterUserUseCase, LoginUserUseCase, VerifyCodeUseCase, SendCodeUseCase
from src.infrastructure.repositories.user.base import BaseBlockedUserRepository, BaseUserRepository
from src.infrastructure.repositories.user.blocked_user import BlockedUserRepository
from src.infrastructure.repositories.user.sqlalchemy import SQLAlchemyUserRepository
from src.infrastructure.cache.base import BaseCacheService
from src.infrastructure.cache.redis import RedisCacheService
from src.presentation.schemas.jwt_token import AccessTokenReponse
from src.application.services.code import CheckCodeService, SendCodeService
from src.domain.jwt.exception import TokenAbsentException


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
    
    @provide(scope=Scope.REQUEST)
    def get_blocked_user_repository(self, session: AsyncSession) -> BaseBlockedUserRepository:

        return BlockedUserRepository(_session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_bots_repository(self, session: AsyncSession) -> BaseBotRepository:

        return SQLAlchemyBotRepository(_session=session)


    #USE CASES
    @provide(scope=Scope.REQUEST)
    def get_send_code_use_case(
        self,
        send_code_service: SendCodeService,
    ) -> SendCodeUseCase:
        
        return SendCodeUseCase(_send_code_service=send_code_service)

    @provide(scope=Scope.REQUEST)
    def get_verify_code_use_case(
        self,
        check_code_service: CheckCodeService,
        login_user_use_case: LoginUserUseCase,
        register_user_use_case: RegisterUserUseCase,
        user_repository: BaseUserRepository,
    ) -> VerifyCodeUseCase:
        
        return VerifyCodeUseCase(
            _check_code=check_code_service,
            _login_use_case=login_user_use_case,
            _register_use_case=register_user_use_case,
            _user_repository=user_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_refresh_token_use_case(
        self,
        jwt_service: JWTService,
    ) -> RefreshTokenUseCase:
        
        return RefreshTokenUseCase(_jwt_service=jwt_service)

    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(
        self,
        user_repository: BaseUserRepository,
        jwt_service: JWTService,
    ) -> RegisterUserUseCase:
        
        return RegisterUserUseCase(
            _user_repository=user_repository,
            _jwt_service=jwt_service,
        )
    
    @provide(scope=Scope.REQUEST)
    def get_login_user_use_case(
        self,
        user_repository: BaseUserRepository,
        jwt_service: JWTService,
    ) -> LoginUserUseCase:
        
        return LoginUserUseCase(_user_repository=user_repository, _jwt_service=jwt_service)
    
    @provide(scope=Scope.REQUEST)
    def get_all_users_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> GetAllUsersUseCase:
        
        return GetAllUsersUseCase(_user_repository=user_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_users_by_telegram_id_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> GetUserByTelegramId:
        
        return GetUserByTelegramId(_user_repository=user_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_delete_user_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> DeleteUserUseCase:
        
        return DeleteUserUseCase(_user_repository=user_repository)
    

    @provide(scope=Scope.REQUEST)
    def get_update_user_role_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> UpdateUserRoleUseCase:
        
        return UpdateUserRoleUseCase(_user_repository=user_repository)


    @provide(scope=Scope.REQUEST)
    def get_block_user_use_case(
        self,
        user_repository: BaseUserRepository,
        blocked_user_repository: BaseBlockedUserRepository,
    ) -> BlockUserUseCase:
        
        return BlockUserUseCase(
            _user_repository=user_repository,
            _blocked_user_repository=blocked_user_repository,
        )
    
    @provide(scope=Scope.REQUEST)
    def get_unblock_user_use_case(
        self,
        user_repository: BaseUserRepository,
        blocked_user_repository: BaseBlockedUserRepository,
    ) -> UnblockUserUseCase:
        
        return UnblockUserUseCase(
            _user_repository=user_repository,
            _blocked_user_repository=blocked_user_repository,
        )
    
    @provide(scope=Scope.REQUEST)
    def get_create_bot_use_case(
        self,
        bot_repository: BaseBotRepository,
    ) -> CreateNewBotUseCase:
        
        return CreateNewBotUseCase(_bot_repository=bot_repository)
        
    @provide(scope=Scope.REQUEST)
    def get_all_bots_use_case(
        self,
        bot_repository: BaseBotRepository,
    ) -> GetAllBotsUseCase:
        
        return GetAllBotsUseCase(_bot_repository=bot_repository)
    

    @provide(scope=Scope.REQUEST)
    def get_all_bots_with_rentals(
        self,
        bot_repository: BaseBotRepository,
    ) -> GetAllBotsWithRentalsUseCase:
        
        return GetAllBotsWithRentalsUseCase(_bot_repository=bot_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_delete_bot_use_case(
        self,
        bot_repository: BaseBotRepository,
    ) -> DeleteBotUseCase:
        
        return DeleteBotUseCase(_bot_repository=bot_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_update_bot_use_case(
        self,
        bot_repository: BaseBotRepository,
    ) -> UpdateBotUseCase:
        
        return UpdateBotUseCase(_bot_repository=bot_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_activate_bot_use_case(
        self,
        bot_repository: BaseBotRepository,
    ) -> ActivateBotUseCase:
        
        return ActivateBotUseCase(_bot_repository=bot_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_deactivate_bot_use_case(
        self,
        bot_repository: BaseBotRepository,
    ) -> DeactivateBotUseCase:
        
        return DeactivateBotUseCase(_bot_repository=bot_repository)

    #SERVICES
    @provide(scope=Scope.REQUEST)
    def get_cache_service(
        self,
    ) -> BaseCacheService:
        
        return RedisCacheService()
    
    @provide(scope=Scope.REQUEST)
    def get_jwt_service(
        self,
        config: Config,
    ) -> JWTService:
        
        return JWTServiceImpl(config=config)
    
    @provide(scope=Scope.REQUEST)
    def get_send_code_service(
        self,
        cache_service: BaseCacheService,
    ) -> SendCodeService:
        
        return SendCodeService(_cache_service=cache_service)
        
    @provide(scope=Scope.REQUEST)
    def get_check_code_service(
        self,
        cache_service: BaseCacheService,
    ) -> CheckCodeService:
        
        return CheckCodeService(
            _cache_service=cache_service,
        )

    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self,
        user_repository: BaseUserRepository,
        jwt_service: JWTService,
        cache_service: BaseCacheService,
    ) -> BaseAuthService:
        
        return AuthServiceImpl(
            _user_repository=user_repository,
            _jwt_service=jwt_service,
            _cache_service=cache_service,
        )

    #current user
    @provide(scope=Scope.REQUEST)
    def get_access_token(self, request: Request) -> AccessTokenReponse:
        token: str | None = request.cookies.get('access_token')
        if not token:
            raise TokenAbsentException()
        return AccessTokenReponse(token=token)

    
    @provide(scope=Scope.REQUEST)
    async def get_current_user(
        self,
        auth_service: BaseAuthService,
        access_token: AccessTokenReponse,
    ) -> UserEntity:
        
        if not access_token:
            return None

        user: UserEntity | None = await auth_service.get_current_user(token=access_token.token)
        if not user:
            return None
        return user