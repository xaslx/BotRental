from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.domain.user.entity import Role
from datetime import datetime


class CheckCodeSchema(BaseModel):
    telegram_id: int = Field(gt=0)
    confirmation_code: int


class SendCodeSchema(BaseModel):
    telegram_id: int = Field(gt=0)
    ref_id: int | None = None


class BlockedUserOutSchema(BaseModel):
    created_at: datetime
    user_id: int
    blocked_until: datetime
    reason: str
    blocked_by: int

    model_config = ConfigDict(from_attributes=True)


class BotRentalOutSchema(BaseModel):
    id: int
    bot_id: int
    user_id: int
    rented_until: datetime
    token: str
    rented_until: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ReferralOutSchema(BaseModel):
    id: int | None
    referrer_id: int
    referral_id: int
    telegram_id: int
    invited_at: datetime
    total_bonus: int

    model_config = ConfigDict(from_attributes=True)

class UserOutSchema(BaseModel):
    id: int
    created_at: datetime
    telegram_id: int
    balance: int
    blocks: list[BlockedUserOutSchema]
    referrer_id: int | None
    total_bonus_received: int

    model_config = ConfigDict(from_attributes=True)


class UserAdminViewSchema(UserOutSchema):
    is_deleted: bool
    role: Role
    rentals: list[BotRentalOutSchema] | None
    referrals: list[ReferralOutSchema] | None

    model_config = ConfigDict(from_attributes=True)



class UpdateUserRole(BaseModel):
    role: Role


class UserBlockSchema(BaseModel):
    reason: str
    days: int
