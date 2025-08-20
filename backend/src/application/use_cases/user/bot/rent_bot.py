from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.cache.base import BaseCacheService
from src.presentation.schemas.bot import CreateBotRentSchema
from src.domain.bot.entity import BotEntity, BotRentalEntity
from src.domain.bot.exception import BotCannotBeRentedException, BotNotFoundException
from src.domain.user.entity import UserEntity
from src.infrastructure.repositories.bot.base import BaseBotRepository
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.const import MOSCOW_TZ
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.infrastructure.repositories.rental.base import BaseRentalRepository



@dataclass
class RentBotUseCase:
    _bot_repository: BaseBotRepository
    _user_repository: BaseUserRepository
    _bot_rental_repository: BaseRentalRepository
    _cache_service: BaseCacheService
    _session: AsyncSession

    async def execute(self, bot_id: int, user: UserEntity, schema: CreateBotRentSchema) -> BotRentalEntity:

        bot: BotEntity | None = await self._bot_repository.get_bot_by_id(bot_id)

        if not bot:
            raise BotNotFoundException()
        
        if not bot.is_available:
            raise BotCannotBeRentedException()

        
        now: datetime = datetime.now(MOSCOW_TZ)
        rented_until: datetime = now + relativedelta(months=schema.months)
        rental_entity = BotRentalEntity.create_rental(
            user_id=user.id,
            bot_id=bot.id,
            token=schema.token,
            rented_until=rented_until,
            user=user,
            bot=bot
        )

        await self._bot_rental_repository.add(rental_entity)

        user.withdraw(bot.price.to_raw())
        user.add_rental(rental_entity)

        await self._user_repository.update(user)
        await self._session.commit()
        await self._cache_service.delete(key=f'user:{str(user.telegram_id.to_raw())}')

        return rental_entity
        